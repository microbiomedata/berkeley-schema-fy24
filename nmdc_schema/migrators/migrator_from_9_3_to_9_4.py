from nmdc_schema.migrators.migrator_base import MigratorBase


class Migrator(MigratorBase):
    r"""Migrates data between two schema versions."""

    _from_version = "9.3"
    _to_version = "9.4"

    def __init__(self, *args, **kwargs) -> None:
        super().__init__(*args, **kwargs)
        self._agenda = dict(
            extraction_set=[self.move_extraction_qc_status],
        )

    def move_extraction_qc_status(self, extraction: dict) -> dict:
        r"""
        Updates the `Extraction` so that the value originally in its `quality_control_report.status` field, if any,
        is stored in a new field named `qc_status`; and the `quality_control_report` field no longer exists.

        >>> m = Migrator()
        >>> m.move_extraction_qc_status({'id': 123, 'quality_control_report': {'status': 'pass'}})
        {'id': 123, 'qc_status': 'pass'}
        >>> m.move_extraction_qc_status({'id': 123, 'quality_control_report': {'status': 'fail'}})
        {'id': 123, 'qc_status': 'fail'}
        >>> m.move_extraction_qc_status({'id': 123, 'quality_control_report': {'status': 'pass', 'name': 'n'}})
        {'id': 123, 'qc_status': 'pass'}
        >>> m.move_extraction_qc_status({'id': 123, 'quality_control_report': {'status': 'fail', 'name': 'n'}})
        {'id': 123, 'qc_status': 'fail'}
        >>> m.move_extraction_qc_status({'id': 123, 'quality_control_report': {'name': 'n'}})
        {'id': 123}
        >>> m.move_extraction_qc_status({'id': 123, 'quality_control_report': {}})
        {'id': 123}
        """
        self.logger.info(f"Migrating Extraction: {extraction['id']}")
        if "quality_control_report" in extraction:
            if "status" in extraction["quality_control_report"]:
                extraction["qc_status"] = extraction["quality_control_report"]["status"]

            # Delete the key, even if it contains sub-keys other than "status".
            del extraction["quality_control_report"]
        return extraction
