# -*- coding: utf-8 -*-
import json
import logging
import os
import re
import tempfile
import stat

import docker
import pytest
import yaml
from packaging import version

from click.testing import CliRunner

from gordo.workflow.workflow_generator import workflow_generator as wg
from gordo import cli
from gordo.workflow.config_elements.normalized_config import NormalizedConfig
from gordo.workflow.workflow_generator.workflow_generator import (
    default_image_pull_policy,
)
from gordo.util.version import GordoRelease, GordoSpecial, GordoPR, GordoSHA, Special
from gordo.machine.loader import load_model_config, load_machine_config
from typing import List


logger = logging.getLogger(__name__)


@pytest.fixture(scope="session")
def path_to_config_files():
    """
    Return the data path containing workflow generator test configuration files
    """
    return os.path.join(os.path.dirname(__file__), "data")


def _generate_test_workflow_yaml(
    path_to_config_files, config_filename, project_name="test-proj-name", args=None
):
    """
    Reads a test-config file with workflow_generator, and returns the parsed
    yaml of the generated workflow
    """
    getvalue = _generate_test_workflow_str(
        path_to_config_files, config_filename, project_name=project_name, args=args
    )
    expanded_template = yaml.load(getvalue, Loader=yaml.FullLoader)

    return expanded_template


def _create_executable_with_output(file_path: str, output: str):
    # Only Unix like
    # TODO Port to Windows
    with open(file_path, "w") as f:
        f.write("#!/usr/bin/env bash\n")
        f.write('echo "%s"\n' % output)
    s = os.stat(file_path)
    os.chmod(file_path, s.st_mode | stat.S_IXUSR | stat.S_IXGRP | stat.S_IXOTH)


def _run_workflow_generate(args, argo_version="2.1.0", argo_binary="argo"):
    with tempfile.TemporaryDirectory() as tmp_directory:
        path = os.environ["PATH"]
        cli_path = tmp_directory + os.pathsep + path
        temp_bin = os.path.join(tmp_directory, argo_binary)
        _create_executable_with_output(temp_bin, "argo: v%s" % argo_version)
        cli_args = [
            "workflow",
            "generate",
        ]
        cli_args.extend(args)
        runner = CliRunner(env={"PATH": cli_path})

        return runner.invoke(cli.gordo, cli_args)


def _generate_test_workflow_str(
    path_to_config_files,
    config_filename,
    project_name="test-proj-name",
    args=None,
    argo_version="2.1.0",
    argo_binary="argo",
):
    """
    Reads a test-config file with workflow_generator, and returns the string
    content of the generated workflow
    """
    config_file = os.path.join(path_to_config_files, config_filename)
    additional_args = [
        "--machine-config",
        config_file,
        "--project-name",
        project_name,
    ]
    if args is not None:
        additional_args.extend(args)
    result = _run_workflow_generate(
        additional_args,
        argo_version,
        argo_binary,
    )

    if result.exception is not None:
        raise result.exception
    return result.output


def _get_env_for_machine_build_serve_task(machine, expanded_template):
    templates = expanded_template["spec"]["templates"]
    do_all = [task for task in templates if task["name"] == "do-all"][0]
    model_builder_machine = [
        task
        for task in do_all["dag"]["tasks"]
        if task["name"] == f"model-builder-{machine}"
    ][0]
    model_builder_machine_env = {
        e["name"]: e["value"] for e in model_builder_machine["arguments"]["parameters"]
    }
    return model_builder_machine_env


def _get_do_all_tasks(config):
    templates = config["spec"]["templates"]
    do_all_template = [
        template for template in templates if template["name"] == "do-all"
    ][0]
    return do_all_template["dag"]["tasks"]


def _filter_gordo_model_config_parameter(tasks):
    filtered_task_parameters = [
        task["arguments"]["parameters"]
        for task in tasks
        if task["template"] == "gordo-model"
    ]
    for parameters in filtered_task_parameters:
        for parameter in parameters:
            if parameter["name"] == "config":
                yield yaml.safe_load(parameter["value"])


def test_basic_generation(path_to_config_files):
    """
    Model must be included in the config file

    start/end dates ...always included? or default to specific dates if not included?
    """

    project_name = "some-fancy-project-name"
    model_config = '{"sklearn.pipeline.Pipeline": {"steps": ["sklearn.preprocessing.MinMaxScaler", {"gordo.machine.model.models.KerasAutoEncoder": {"kind": "feedforward_hourglass"}}]}}'

    config_filename = "config-test-with-models.yml"
    expanded_template = _generate_test_workflow_str(
        path_to_config_files, config_filename, project_name=project_name
    )

    assert (
        project_name in expanded_template
    ), f"Expected to find project name: {project_name} in output: {expanded_template}"

    do_all_templates = _get_do_all_tasks(yaml.safe_load(expanded_template))

    for config in _filter_gordo_model_config_parameter(do_all_templates):
        machine = load_machine_config(config)
        model = json.dumps(machine["model"])
        assert (
            model_config in model
        ), f"Expected to find model config: {model_config} in machine {machine['name']}"

    yaml_content = wg.get_dict_from_yaml(
        os.path.join(path_to_config_files, config_filename)
    )

    machines = NormalizedConfig(yaml_content, project_name=project_name).machines

    assert len(machines) == 2


def test_generation_to_file(tmpdir, path_to_config_files):
    """
    Test that the workflow generator can output to a file, and it matches
    what would have been output to stdout.
    """
    project_name = "my-sweet-project"
    config_filename = "config-test-with-models.yml"
    expanded_template = _generate_test_workflow_str(
        path_to_config_files, config_filename, project_name=project_name
    )

    # Execute CLI by passing a file to write to.
    config_file = os.path.join(path_to_config_files, config_filename)
    outfile = os.path.join(tmpdir, "out.yml")

    args = [
        "--machine-config",
        config_file,
        "--project-name",
        project_name,
        "--output-file",
        outfile,
    ]
    result = _run_workflow_generate(args)
    assert result.exit_code == 0

    # Open the file and ensure they are the same
    with open(outfile, "r") as f:
        outfile_contents = f.read()
    assert outfile_contents.rstrip() == expanded_template.rstrip()


def test_quotes_work(path_to_config_files):
    """Tests that quotes various places result in valid yaml"""
    expanded_template = _generate_test_workflow_yaml(
        path_to_config_files, "config-test-quotes.yml"
    )
    model_builder_machine_1_env = _get_env_for_machine_build_serve_task(
        "machine-1", expanded_template
    )

    machine_1_metadata = yaml.safe_load(model_builder_machine_1_env["machine"])
    machine_1_model = load_model_config(machine_1_metadata)
    assert machine_1_model["metadata"]["user_defined"]["machine-metadata"] == {
        "withSingle": "a string with ' in it",
        "withDouble": 'a string with " in it',
        "single'in'key": "why not",
    }

    assert machine_1_model["dataset"]["tag_list"] == ["CT/1", 'CT"2', "CT'3"]


def test_overrides_builder_datasource(path_to_config_files):
    expanded_template = _generate_test_workflow_yaml(
        path_to_config_files, "config-test-datasource.yml"
    )

    model_builder_machine_1_env = _get_env_for_machine_build_serve_task(
        "machine-1", expanded_template
    )
    model_builder_machine_2_env = _get_env_for_machine_build_serve_task(
        "machine-2", expanded_template
    )
    model_builder_machine_3_env = _get_env_for_machine_build_serve_task(
        "machine-3", expanded_template
    )

    # ct_23_0002 uses the global overriden requests, but default limits
    model = load_model_config(yaml.safe_load(model_builder_machine_1_env["machine"]))
    assert {
        "type": "gordo_core.data_providers.providers.RandomDataProvider",
        "max_size": 300,
        "min_size": 100,
    } == model["dataset"]["data_provider"]

    # This value must be changed if we change the default values
    model = load_model_config(yaml.safe_load(model_builder_machine_2_env["machine"]))
    assert {
        "type": "gordo_core.data_providers.providers.RandomDataProvider",
        "max_size": 300,
        "min_size": 100,
    } == model["dataset"]["data_provider"]

    # ct_23_0003 uses locally overriden request memory
    model = load_model_config(yaml.safe_load(model_builder_machine_3_env["machine"]))
    assert {
        "type": "gordo_core.data_providers.providers.RandomDataProvider",
        "max_size": 300,
        "min_size": 100,
    } == model["dataset"]["data_provider"]


def test_builder_labels(path_to_config_files):
    expanded_template = _generate_test_workflow_yaml(
        path_to_config_files, "config-test-runtime-labels.yaml"
    )
    templates = expanded_template["spec"]["templates"]
    model_builder_task = [
        task for task in templates if task["name"] == "model-builder"
    ][0]
    assert "key1" in model_builder_task["metadata"]["labels"]
    assert "value1" == model_builder_task["metadata"]["labels"]["key1"]

    assert "key2" in model_builder_task["metadata"]["labels"]
    assert "2" == model_builder_task["metadata"]["labels"]["key2"]

    assert "key3/withslash" in model_builder_task["metadata"]["labels"]
    assert "value3" == model_builder_task["metadata"]["labels"]["key3/withslash"]

    assert "key4/withslash.dot" in model_builder_task["metadata"]["labels"]
    assert "value4" == model_builder_task["metadata"]["labels"]["key4/withslash.dot"]


def filter_keys(input_list: list, key: str, values: List[str]) -> list:
    output_list = []
    for v in input_list:
        find_v = v[key]
        if find_v in values:
            output_list.append(v)
    return output_list


@pytest.mark.parametrize(
    "template_name,spec_key",
    [("model-builder", "container"), ("gordo-client", "script")],
)
def test_model_builder_spec(path_to_config_files, template_name, spec_key):
    expanded_template = _generate_test_workflow_yaml(
        path_to_config_files, "config-test-model-builder-spec.yaml"
    )
    templates = expanded_template["spec"]["templates"]
    volumes = expanded_template["spec"]["volumes"]
    template = [task for task in templates if task["name"] == template_name][0]
    labels = template["metadata"]["labels"]
    env = template[spec_key]["env"]
    volume_mounts = template[spec_key]["volumeMounts"]
    assert labels["key1"] == "value1"
    assert labels["key2"] == "value2"
    assert filter_keys(env, "name", ["DL_PWD"]) == [
        {
            "name": "DL_PWD",
            "valueFrom": {
                "secretKeyRef": {"key": "deltalake-pwd", "name": "deltalake-pwd"}
            },
        }
    ]
    assert filter_keys(volumes, "name", ["secrets-store"]) == [
        {
            "csi": {
                "driver": "secrets-store.csi.k8s.io",
                "readOnly": True,
                "volumeAttributes": {"secretProviderClass": "kv-sync"},
            },
            "name": "secrets-store",
        }
    ]
    assert filter_keys(volume_mounts, "name", ["secrets-store"]) == [
        {"mountPath": "/kvmnt", "name": "secrets-store", "readOnly": True}
    ]


def test_runtime_image_override(path_to_config_files):
    expanded_template = _generate_test_workflow_yaml(
        path_to_config_files, "config-test-runtime-images.yaml"
    )
    templates = expanded_template["spec"]["templates"]
    model_builder_task = [
        task for task in templates if task["name"] == "model-builder"
    ][0]
    model_builder_image = model_builder_task["container"]["image"]
    actual_model_builder_image = model_builder_image.split("/")[-1].split(":")[0]
    assert actual_model_builder_image == "new-builder-image"

    client_task = [task for task in templates if task["name"] == "gordo-client"][0]
    client_task_image = client_task["script"]["image"]
    actual_client_task_image = client_task_image.split("/")[-1].split(":")[0]
    assert actual_client_task_image == "new-client-image"

    server_task = [
        task for task in templates if task["name"] == "gordo-server-deployment"
    ][0]
    server_task_deployment = server_task["steps"][0][0]["arguments"]["parameters"][0][
        "value"
    ]
    server_task_yaml = yaml.load(server_task_deployment)
    actual_server_task_image = (
        server_task_yaml["spec"]["template"]["spec"]["containers"][0]["image"]
        .split("/")[-1]
        .split(":")[0]
    )
    assert actual_server_task_image == "new-server-image"


def test_runtime_overrides_builder(path_to_config_files):
    expanded_template = _generate_test_workflow_yaml(
        path_to_config_files, "config-test-runtime-resource.yaml"
    )
    templates = expanded_template["spec"]["templates"]
    model_builder_task = [
        task for task in templates if task["name"] == "model-builder"
    ][0]
    model_builder_resource = model_builder_task["container"]["resources"]

    # We use yaml overriden memory (both request and limits).
    assert model_builder_resource["requests"]["memory"] == "121M"

    # This was specified to 120 in the config file, but is bumped to match the
    # request
    assert model_builder_resource["limits"]["memory"] == "121M"
    # requests.cpu is all default
    assert model_builder_resource["requests"]["cpu"] == "1001m"


def test_runtime_overrides_client_para(path_to_config_files):
    """
    It is possible to override the parallelization of the client
    through the globals-section of the config file
    """
    expanded_template = _generate_test_workflow_yaml(
        path_to_config_files, "config-test-runtime-resource.yaml"
    )
    templates = expanded_template["spec"]["templates"]
    client_task = [task for task in templates if task["name"] == "gordo-client-waiter"][
        0
    ]

    client_env = {e["name"]: e["value"] for e in client_task["script"]["env"]}

    assert client_env["GORDO_MAX_CLIENTS"] == "10"


def test_runtime_overrides_client(path_to_config_files):
    expanded_template = _generate_test_workflow_yaml(
        path_to_config_files, "config-test-runtime-resource.yaml"
    )
    templates = expanded_template["spec"]["templates"]
    model_client_task = [task for task in templates if task["name"] == "gordo-client"][
        0
    ]
    model_client_resource = model_client_task["script"]["resources"]

    # We use yaml overriden memory (both request and limits).
    assert model_client_resource["requests"]["memory"] == "221M"

    # This was specified to 120 in the config file, but is bumped to match the
    # request
    assert model_client_resource["limits"]["memory"] == "221M"
    # requests.cpu is all default
    assert model_client_resource["requests"]["cpu"] == "100m"


def test_runtime_overrides_influx(path_to_config_files):
    expanded_template = _generate_test_workflow_yaml(
        path_to_config_files, "config-test-runtime-resource.yaml"
    )
    templates = expanded_template["spec"]["templates"]
    influx_task = [
        task for task in templates if task["name"] == "gordo-influx-statefulset"
    ][0]
    influx_statefulset_definition = yaml.load(
        influx_task["resource"]["manifest"], Loader=yaml.FullLoader
    )
    influx_resource = influx_statefulset_definition["spec"]["template"]["spec"][
        "containers"
    ][0]["resources"]
    # We use yaml overriden memory (both request and limits).
    assert influx_resource["requests"]["memory"] == "321M"

    # This was specified to 120 in the config file, but is bumped to match the
    # request
    assert influx_resource["limits"]["memory"] == "321M"
    # requests.cpu is default
    assert influx_resource["requests"]["cpu"] == "520m"
    assert influx_resource["limits"]["cpu"] == "10040m"


def test_disable_influx(path_to_config_files):
    """
    It works to disable influx globally
    """
    expanded_template = _generate_test_workflow_yaml(
        path_to_config_files, "config-test-disable-influx.yml"
    )
    templates = expanded_template["spec"]["templates"]
    do_all = [task for task in templates if task["name"] == "do-all"][0]
    influx_tasks = [
        task["name"] for task in do_all["dag"]["tasks"] if "influx" in task["name"]
    ]
    client_tasks = [
        task["name"] for task in do_all["dag"]["tasks"] if "client" in task["name"]
    ]

    # The cleanup should be the only influx-related task
    assert influx_tasks == ["influx-cleanup"]
    assert client_tasks == []


def test_selective_influx(path_to_config_files):
    """
    It works to enable/disable influx per machine
    """
    expanded_template = _generate_test_workflow_yaml(
        path_to_config_files, "config-test-selective-influx.yml"
    )
    templates = expanded_template["spec"]["templates"]
    do_all = [task for task in templates if task["name"] == "do-all"][0]
    influx_tasks = [
        task["name"] for task in do_all["dag"]["tasks"] if "influx" in task["name"]
    ]
    client_tasks = [
        task["name"] for task in do_all["dag"]["tasks"] if "client" in task["name"]
    ]

    # Now we should have both influx and influx-cleanup
    assert influx_tasks == ["influx-cleanup", "gordo-influx"]

    # And we have a single client task for the one client we want running
    assert client_tasks == ["gordo-client-ct-23-0002"]


def test_valid_dateformats(path_to_config_files):
    output_workflow = _generate_test_workflow_str(
        path_to_config_files, "config-test-allowed-timestamps.yml"
    )
    # Three from the dataset, three from the start for tag fetching, and three in
    # each machine's model-crd specification
    assert output_workflow.count("2016-11-07") == 9
    assert output_workflow.count("2017-11-07") == 6


def test_model_names_embedded(path_to_config_files):
    """
    Tests that the generated workflow contains the names of the machines
    it builds a workflow for in the metadata/annotation as a yaml-parsable structure
    """
    output_workflow = _generate_test_workflow_yaml(
        path_to_config_files, "config-test-allowed-timestamps.yml"
    )
    parsed_machines = yaml.load(
        output_workflow["metadata"]["annotations"]["gordo-models"],
        Loader=yaml.FullLoader,
    )
    assert parsed_machines == ["machine-1", "machine-2", "machine-3"]


def test_missing_timezone(path_to_config_files):
    with pytest.raises(ValueError):
        _generate_test_workflow_yaml(
            path_to_config_files, "config-test-missing-timezone.yml"
        )

    with pytest.raises(ValueError):
        _generate_test_workflow_yaml(
            path_to_config_files, "config-test-missing-timezone-quoted.yml"
        )


def test_validates_resource_format(path_to_config_files):
    """
    We validate that resources are integers
    """
    with pytest.raises(ValueError):
        _generate_test_workflow_str(
            path_to_config_files, "config-test-failing-resource-format.yml"
        )


@pytest.mark.parametrize(
    "owner_ref_str,valid",
    (
        ("[]", False),
        ("- key: value", False),
        (
            """
            - uid: 1
              name: name
              kind: kind
              apiVersion: v1
            """,
            True,
        ),
    ),
)
def test_valid_owner_ref(owner_ref_str: str, valid: bool):
    if valid:
        wg._valid_owner_ref(owner_ref_str)
    else:
        with pytest.raises(TypeError):
            wg._valid_owner_ref(owner_ref_str)


@pytest.mark.parametrize(
    "test_file, log_level",
    (
        ("config-test-with-log-key.yml", "DEBUG"),
        ("config-test-with-models.yml", "INFO"),
    ),
)
def test_log_level_key(test_file: str, log_level: str, path_to_config_files: str):
    """
    Test that GORDO_LOG_LEVEL is set to the correct value if specified in the config file, or default to INFO if not
    specified.
    """
    workflow_str = _generate_test_workflow_str(path_to_config_files, test_file)

    # Find the value on the next line after the key GORDO_LOG_LEVEL
    gordo_log_levels = re.findall(
        r"(?<=GORDO_LOG_LEVEL\r|GORDO_LOG_LEVEL\n)[^\r\n]+", workflow_str
    )

    # Assert all the values to the GORDO_LOG_LEVEL key contains the correct log-level
    assert all([log_level in value for value in gordo_log_levels])


def test_expected_models_in_workflow(repo_dir):
    """
    Server deployment depends on EXPECTED_MODELS env var being set,
    which is a list of strings, indicating the expected model names to be served.
    """
    workflow_str = _generate_test_workflow_str(
        path_to_config_files=os.path.join(repo_dir, "examples"),
        config_filename="config.yaml",
    )
    assert "name: EXPECTED_MODELS" in workflow_str

    # Not the prettiest, but a whole lot prettier than digging down into the workflow yaml
    # basically want to get to 'gordo-server-deployment' and ensure the EXPECTED_MODELS env var
    # is set with a list (in string form) of model names which can be loaded.
    expected_models_str = (
        workflow_str.split("EXPECTED_MODELS")[1]
        .split("value:")[1]
        .split("|")[1]
        .split()[0]
    )
    assert isinstance(yaml.safe_load(expected_models_str), list)


@pytest.mark.parametrize(
    "gordo_version,expected",
    [
        (GordoRelease(2, 10, 23), "IfNotPresent"),
        (GordoRelease(1, 2), "Always"),
        (GordoRelease(10), "Always"),
        (GordoSpecial(Special.LATEST), "Always"),
        (GordoPR(43), "Always"),
        (GordoSHA("dke0832k"), "IfNotPresent"),
    ],
)
def test_default_image_pull_policy(gordo_version, expected):
    result = default_image_pull_policy(gordo_version)
    assert result == expected


def _get_names_recursively(steps: list) -> list:
    names = []
    for step in steps:
        if type(step) is list:
            names.extend(_get_names_recursively(step))
        else:
            names.append(step["name"])
    return names


@pytest.mark.parametrize(
    "args,expected_steps",
    [
        ([], ["gordo-server-hpa"]),
        (["--with-keda"], ["gordo-server-hpa", "gordo-server-keda-cleanup"]),
        (["--ml-server-hpa-type", "none"], ["gordo-server-hpa-cleanup"]),
        (
            ["--with-keda", "--ml-server-hpa-type", "none"],
            ["gordo-server-keda-cleanup", "gordo-server-hpa-cleanup"],
        ),
        (["--ml-server-hpa-type", "k8s_cpu"], ["gordo-server-hpa"]),
        (
            ["--with-keda", "--ml-server-hpa-type", "k8s_cpu"],
            ["gordo-server-hpa", "gordo-server-keda-cleanup"],
        ),
        (
            [
                "--with-keda",
                "--ml-server-hpa-type",
                "keda",
                "--prometheus-server-address",
                "http://prometheus.local",
            ],
            ["gordo-server-keda", "gordo-server-hpa-cleanup"],
        ),
    ],
)
def test_hpa_types(path_to_config_files: str, args: list, expected_steps: list):
    workflow_str = _generate_test_workflow_str(
        path_to_config_files, "config-test-simple.yml", args=args
    )
    workflow = yaml.safe_load(workflow_str)
    templates = workflow["spec"]["templates"]
    gordo_server_step = [step for step in templates if step["name"] == "gordo-server"][
        0
    ]
    names = _get_names_recursively(gordo_server_step["steps"])
    for expected_step in expected_steps:
        assert (
            expected_step in names
        ), "Unable to found expected gordo-server step '%s' with args: %s" % (
            expected_step,
            " ".join(args),
        )


def recurse_dict(value):
    if type(value) is list:
        for item in value:
            for k, v in recurse_dict(item):
                yield k, v
    elif type(value) is dict:
        for k, v in value.items():
            for k1, v1 in recurse_dict(v):
                yield k1, v1
            yield k, v


def test_recurse_dict():
    result = sorted(
        recurse_dict({"b": [{"a": 1}, {"d": [2, {"c": 3}]}]}), key=lambda v: v[0]
    )
    assert result == [
        ("a", 1),
        ("b", [{"a": 1}, {"d": [2, {"c": 3}]}]),
        ("c", 3),
        ("d", [2, {"c": 3}]),
    ]


def test_pod_security_context(path_to_config_files: str):
    args = [
        "--pod-security-context",
        '{"runAsNonRoot": true}',
    ]
    workflow_str = _generate_test_workflow_str(
        path_to_config_files, "config-test-simple.yml", args=args
    )
    workflow = yaml.safe_load(workflow_str)
    assert "securityContext" in workflow["spec"]
    assert workflow["spec"]["securityContext"] == {"runAsNonRoot": True}


def test_security_context(path_to_config_files: str):
    args = [
        "--security-context",
        '{"runAsNonRoot": true, "readOnlyRootFilesystem": true}',
    ]
    workflow_str = _generate_test_workflow_str(
        path_to_config_files, "config-test-simple.yml", args=args
    )
    workflow = yaml.safe_load(workflow_str)
    for k, v in recurse_dict(workflow):
        if k == "securityContext":
            assert v == {
                "readOnlyRootFilesystem": True,
                "runAsNonRoot": True,
            }


def test_security_context_failed(path_to_config_files: str):
    args = [
        "--security-context",
        '{"unknownSecurityParam": true, "readOnlyRootFilesystem": true}',
    ]
    with pytest.raises(SystemExit):
        _generate_test_workflow_str(
            path_to_config_files, "config-test-simple.yml", args=args
        )


def test_with_resources_labels(path_to_config_files: str):
    resources_labels = '{"some_custom_label": "value"}'
    args = ["--resources-labels", resources_labels]
    workflow_str = _generate_test_workflow_str(
        path_to_config_files, "config-test-simple.yml", args=args
    )
    yaml.safe_load(workflow_str)
    expected_str = '"some_custom_label": "value"'
    assert workflow_str.find(
        expected_str
    ), 'Unable to find label "some_custom_label" in the generated argo-workflow'


def test_default_data_provider(path_to_config_files: str):
    args = ["--default-data-provider", "RandomDataProvider"]
    workflow_str = _generate_test_workflow_str(
        path_to_config_files, "config-empty-default-data-provider.yml", args=args
    )
    assert "gordo_core.data_providers.providers.RandomDataProvider" in workflow_str


def test_for_argo_version_3(path_to_config_files: str):
    workflow_str = _generate_test_workflow_str(
        path_to_config_files, "config-test-simple.yml", argo_version="3.0.0"
    )
    assert "secondsAfterCompletion" in workflow_str


def test_argo3_binary(path_to_config_files: str):
    _generate_test_workflow_str(
        path_to_config_files,
        "config-test-simple.yml",
        args=["--argo-binary", "argo3"],
        argo_binary="argo3",
        argo_version="3.1.0",
    )


def test_model_builder_labels(path_to_config_files: str):
    workflow_str = _generate_test_workflow_str(
        path_to_config_files,
        "config-test-simple.yml",
        args=[
            "--model-builder-labels",
            '{"model-builder-label1": "value1", "model-builder-label2": "value2"}',
        ],
    )
    workflow = yaml.safe_load(workflow_str)
    templates = workflow["spec"]["templates"]
    model_builder_step = [
        step for step in templates if step["name"] == "model-builder"
    ][0]
    labels = model_builder_step["metadata"]["labels"]
    assert labels["model-builder-label1"] == "value1"
    assert labels["model-builder-label2"] == "value2"


def test_model_server_(path_to_config_files: str):
    workflow_str = _generate_test_workflow_str(
        path_to_config_files,
        "config-test-simple.yml",
        args=[
            "--server-labels",
            '{"server-label1": "value1", "server-label2": "value2"}',
        ],
    )
    workflow = yaml.safe_load(workflow_str)
    templates = workflow["spec"]["templates"]
    gordo_server_step = [
        step for step in templates if step["name"] == "gordo-server-deployment"
    ][0]
    parameters = gordo_server_step["steps"][0][0]["arguments"]["parameters"]
    resource_step = [v for v in parameters if v["name"] == "resource"][0]
    resource = yaml.safe_load(resource_step["value"])
    labels = resource["metadata"]["labels"]
    assert labels["server-label1"] == "value1"
    assert labels["server-label2"] == "value2"
