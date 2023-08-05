"""Automatic pyfai integration for every scan with saving and plotting"""

import os
import json
from typing import Dict, Optional, Sequence

try:
    from bliss.scanning import scan_meta
    from bliss import current_session
except ImportError:
    scan_meta = None
    current_session = None

from ..persistent import WithPersistentParameters
from ..utils.directories import get_processed_dir


class XrpdProcessor(
    WithPersistentParameters,
    parameters=[
        "_enabled",
        "detector_name",
        "counter_names",
        "pyfai_config",
        "integration_options",
        "retry_timeout",
        "monitor_name",
        "reference",
    ],
):
    def __init__(self) -> None:
        super().__init__()
        if current_session is None:
            raise ImportError("blissdata")
        self._set_parameter_default("_enabled", False)
        self._set_parameter_default(
            "integration_options",
            {
                "method": "no_csr_ocl_gpu",
                "nbpt_rad": 4096,
                "unit": "q_nm^-1",
            },
        )
        self._sync_scan_metadata()

    def _info_categories(self) -> Dict[str, dict]:
        categories = super()._info_categories()
        categories["status"] = {"Enabled": self._enabled}
        return categories

    def enable(
        self,
        detector_name: str,
        counter_names: Optional[Sequence[str]],
        pyfai_config: Optional[str] = None,
        integration_options: Optional[Dict] = None,
    ):
        self._enabled = True
        self.detector_name = detector_name
        self.counter_names = counter_names
        if pyfai_config is not None:
            self.pyfai_config = pyfai_config
        if integration_options is not None:
            self.integration_options = integration_options
        self._sync_scan_metadata()

    def disable(self):
        self._enabled = False
        self._sync_scan_metadata()

    def _sync_scan_metadata(self):
        scan_meta_obj = scan_meta.get_user_scan_meta()
        if self._enabled:
            if "workflows" not in scan_meta_obj.used_categories_names():
                scan_meta_obj.add_categories({"workflows"})
            scan_meta_obj.workflows.timing = scan_meta.META_TIMING.START
            scan_meta_obj.workflows.set("@NX_class", {"@NX_class": "NXcollection"})
            scan_meta_obj.workflows.set("nxprocess1", self.get_nxprocess1_content)
        else:
            try:
                # Before Bliss 1.11
                keys = list(scan_meta_obj._metadata.keys())
                for key in keys:
                    if key.name.lower() == "workflows":
                        scan_meta_obj._metadata.pop(key)
            except Exception:
                pass
            # Since Bliss 1.11
            scan_meta_obj.remove_categories({"workflows"})

    def get_nxprocess1_content(self, scan):
        if not scan.scan_info.get("save"):
            return
        if not scan.scan_info.get("filename"):
            return
        if not scan.scan_info.get("scan_nb"):
            return
        detector_name = self.detector_name
        assert detector_name, "detector name is missing"
        detector_info = scan.scan_info.get("channels", dict()).get(
            f"{detector_name}:image"
        )
        if not detector_info:
            return None
        return {
            "xrpd_data_reduction": {
                "@NX_class": "NXprocess",
                "program": "ewoks",
                "configuration": self.get_configuration(scan),
            }
        }

    def get_configuration(self, scan):
        data = {"workflow": self.get_workflow(), "inputs": self.get_inputs(scan)}
        return {
            "@NX_class": "NXnote",
            "type": "application/json",
            "data": json.dumps(data),
        }

    def get_inputs(self, scan):
        filename = scan.scan_info.get("filename")
        scan_nb = scan.scan_info.get("scan_nb")
        scan_memory_url = f"{scan.root_node.db_name}:{scan._node_name}"
        output_filename = os.path.join(
            get_processed_dir(filename), os.path.basename(filename)
        )
        pyfai_config = self.pyfai_config
        assert pyfai_config, "pyfai configuration is missing"
        detector_name = self.detector_name
        assert detector_name, "detector name is missing"

        integration_options = self.integration_options
        counter_names = self.counter_names
        retry_timeout = self.retry_timeout
        monitor_name = self.monitor_name
        reference = self.reference

        lst = [
            {"id": "config", "name": "filename", "value": pyfai_config},
            {"id": "integrate", "name": "filename", "value": filename},
            {"id": "integrate", "name": "scan", "value": scan_nb},
            {"id": "integrate", "name": "scan_memory_url", "value": scan_memory_url},
            {"id": "integrate", "name": "detector_name", "value": detector_name},
            {"id": "integrate", "name": "output_filename", "value": output_filename},
            {"id": "integrate", "name": "monitor_name", "value": monitor_name},
            {"id": "integrate", "name": "reference", "value": reference},
            {"id": "integrate", "name": "maximum_persistent_workers", "value": 1},
        ]
        if integration_options:
            lst.append(
                {
                    "id": "config",
                    "name": "integration_options",
                    "value": integration_options.to_dict(),
                }
            )
        if counter_names:
            lst.append(
                {"id": "integrate", "name": "counter_names", "value": counter_names}
            )
        if retry_timeout:
            lst.append(
                {"id": "integrate", "name": "retry_timeout", "value": retry_timeout}
            )
        return lst

    def get_workflow(self):
        return {
            "graph": {"id": "xrpd_data_reduction"},
            "nodes": [
                {
                    "id": "config",
                    "task_type": "class",
                    "task_identifier": "ewoksxrpd.tasks.pyfaiconfig.PyFaiConfig",
                },
                {
                    "id": "integrate",
                    "task_type": "class",
                    "task_identifier": "ewoksxrpd.tasks.integrate.IntegrateBlissScan",
                },
            ],
            "links": [
                {
                    "source": "config",
                    "target": "integrate",
                    "data_mapping": [
                        {"source_output": "energy", "target_input": "energy"},
                        {"source_output": "detector", "target_input": "detector"},
                        {
                            "source_output": "detector_config",
                            "target_input": "detector_config",
                        },
                        {"source_output": "geometry", "target_input": "geometry"},
                        {"source_output": "mask", "target_input": "mask"},
                        {
                            "source_output": "integration_options",
                            "target_input": "integration_options",
                        },
                    ],
                }
            ],
        }
