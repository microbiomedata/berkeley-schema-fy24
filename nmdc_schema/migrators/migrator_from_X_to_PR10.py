from nmdc_schema.migrators.migrator_base import MigratorBase
from linkml_runtime import SchemaView
from linkml_runtime.dumpers import yaml_dumper
import nmdc_schema.nmdc_data as nd


class Migrator_from_X_to_PR10(MigratorBase):
    """Migrates data from schema X to PR10"""

    def __init__(self, *args, **kwargs) -> None:
        """Invokes parent constructor and populates collection-to-transformations map."""

        super().__init__(*args, **kwargs)

        # schema_string = nd.get_nmdc_yaml_string()

        # self.view = SchemaView(schema_string)

        # Populate the "collection-to-transformers" map for this specific migration.
        self.agenda = dict(
            biosample_set=[lambda document: self.add_type_slot_with_class_uri(document, "nmdc:Biosample")],
            data_object_set=[lambda document: self.add_type_slot_with_class_uri(document, "nmdc:DataObject")],
            functional_annotation_agg=[
                lambda document: self.add_type_slot_with_class_uri(document, "nmdc:FunctionalAnnotationAggMember")],
            study_set=[lambda document: self.add_type_slot_with_class_uri(document, "nmdc:Study")],
            extraction_set=[lambda document: self.add_type_slot_with_class_uri(document, "nmdc:Extraction")],
            field_research_site_set=[
                lambda document: self.add_type_slot_with_class_uri(document, "nmdc:FieldResearchSite")],
            library_preparation_set=[
                lambda document: self.add_type_slot_with_class_uri(document, "nmdc:LibraryPreparation")],
            mags_activity_set=[lambda document: self.add_type_slot_with_class_uri(document, "nmdc:MagsAnalysis")],
            metabolomics_analysis_activity_set=[
                lambda document: self.add_type_slot_with_class_uri(document, "nmdc:MetabolomicsAnalysis")],
            metagenome_annotation_activity_set=[
                lambda document: self.add_type_slot_with_class_uri(document, "nmdc:MetagenomeAnnotation")],
            metagenome_assembly_set=[
                lambda document: self.add_type_slot_with_class_uri(document, "nmdc:MetagenomeAssembly")],
            metagenome_sequencing_activity_set=[
                lambda document: self.add_type_slot_with_class_uri(document, "nmdc:MetagenomeSequencing")],
            metaproteomics_analysis_activity_set=[
                lambda document: self.add_type_slot_with_class_uri(document, "nmdc:MetaproteomicsAnalysis")],
            metatranscriptome_activity_set=[
                lambda document: self.add_type_slot_with_class_uri(document, "nmdc:MetatranscriptomeAnalysis")],
            nom_analysis_activity_set=[
                lambda document: self.add_type_slot_with_class_uri(document, "nmdc:NomAnalysis")],
            omics_processing_set=[lambda document: self.add_type_slot_with_class_uri(document, "nmdc:DataGeneration")],
            pooling_set=[lambda document: self.add_type_slot_with_class_uri(document, "nmdc:Pooling")],
            processed_sample_set=[lambda document: self.add_type_slot_with_class_uri(document, "nmdc:ProcessedSample")],
            read_based_taxonomy_analysis_activity_set=[
                lambda document: self.add_type_slot_with_class_uri(document, "nmdc:ReadBasedTaxonomyAnalysis")],
            read_qc_analysis_activity_set=[
                lambda document: self.add_type_slot_with_class_uri(document, "nmdc:ReadQcAnalysis")],
        )

    def add_type_to_inlined_classes(self, document: dict, slot: str, uri: str):
        r"""
        Adds a type slot to each inlined instance of an NMDC class in the biosmpale_set collection. This includes nmdc:TextValue,
        nmdc:TimeStampValue, etc. 
        """

        if document.get(slot):
            if isinstance(document[slot], list):
                # If slot is a list, iterate over each item in the list (e.g. chem_administration and has_credit_associations)
                for item in document[slot]:
                    item["type"] = str(uri)
                    if item.get("term"):
                        item["term"]["type"] = "nmdc:OntologyClass"
                    if item.get("applies_to_person"):
                        item["applies_to_person"]["type"] = "nmdc:PersonValue"
            elif isinstance(document[slot], dict):
                # If slot is a dictionary, update the type directly
                document[slot]["type"] = str(uri)
                if document[slot].get("term"):
                    document[slot]["term"]["type"] = "nmdc:OntologyClass"

    def add_type_slot_with_class_uri(self, document: dict, class_uri: str):
        r"""
            Adds a type slot to each collection with the appropriate class uri as the value. E.g. type: nmdc:Biosample. If a type
            slot exists, it will overwrite to the types listed below.
        
            >>> m = Migrator_from_X_to_PR10()
            >>> m.add_type_slot_with_class_uri({'id': 123, 'collection_date': {'has_raw_value': '2017-05-09'}}, 'nmdc:Biosample') 
            {'id': 123, 'collection_date': {'has_raw_value': '2017-05-09', 'type': 'nmdc:TimestampValue'}, 'type': 'nmdc:Biosample'}
            >>> m.add_type_slot_with_class_uri({'id': 567, 'type': 'nmdc:OmicsProcessing'}, 'nmdc:DataGeneration')
            {'id': 567, 'type': 'nmdc:DataGeneration'}
            >>> m.add_type_slot_with_class_uri({'id': 567, 'env_broad_scale': {'term': {'id': 'ENVO:1234'}}}, 'nmdc:Biosample')
            {'id': 567, 'env_broad_scale': {'term': {'id': 'ENVO:1234', 'type': 'nmdc:OntologyClass'}, 'type': 'nmdc:ControlledIdentifiedTermValue'}, 'type': 'nmdc:Biosample'}
            >>> m.add_type_slot_with_class_uri({'id': 456}, 'nmdc:NomAnalysis')
            {'id': 456, 'type': 'nmdc:NomAnalysis'}
        """

        # Adds the type slot with the correct class_uri as a value to each collection instance
        document["type"] = class_uri

        inlined_slots = {
            "collection_date": "nmdc:TimestampValue",
            "depth": "nmdc:QuantityValue",
            "env_broad_scale": "nmdc:ControlledIdentifiedTermValue",
            "env_medium": "nmdc:ControlledIdentifiedTermValue",
            "geo_loc_name": "nmdc:TextValue",
            "lat_lon": "nmdc:GeolocationValue",
            "env_local_scale": "nmdc:ControlledIdentifiedTermValue",
            "temp": "nmdc:QuantityValue",
            "nitrate": "nmdc:QuantityValue",
            "salinity": "nmdc:QuantityValue",
            "subsurface_depth": "nmdc:QuantityValue",
            "env_package": "nmdc:TextValue",
            "host_taxid": "nmdc:ControlledIdentifiedTermValue",
            "samp_taxon_id": "nmdc:ControlledIdentifiedTermValue",
            "ammonium_nitrogen": "nmdc:QuantityValue",
            "calcium": "nmdc:QuantityValue",
            "lbc_thirty": "nmdc:QuantityValue",
            "lbceq": "nmdc:QuantityValue",
            "magnesium": "nmdc:QuantityValue",
            "manganese": "nmdc:QuantityValue",
            "nitrate_nitrogen": "nmdc:QuantityValue",
            "nitrite_nitrogen": "nmdc:QuantityValue",
            "potassium": "nmdc:QuantityValue",
            "tot_nitro": "nmdc:QuantityValue",
            "zinc": "nmdc:QuantityValue",
            "samp_store_temp": "nmdc:QuantityValue",
            "sieving": "nmdc:TextValue",
            "store_cond": "nmdc:TextValue",
            "carb_nitro_ratio": "nmdc:QuantityValue",
            "cur_vegetation": "nmdc:TextValue",
            "tot_phosp": "nmdc:QuantityValue",
            "growth_facil": "nmdc:ControlledTermValue",
            "org_carb": "nmdc:QuantityValue",
            "tot_nitro_content": "nmdc:QuantityValue",
            "nitro": "nmdc:QuantityValue",
            "tot_org_carb": "nmdc:QuantityValue",
            "chem_administration": "nmdc:ControlledTermValue",
            "gravidity": "nmdc:TextValue",
            "host_age": "nmdc:QuantityValue",
            "host_body_habitat": "nmdc:TextValue",
            "host_body_product": "nmdc:ControlledTermValue",
            "host_body_site": "nmdc:ControlledTermValue",
            "host_common_name": "nmdc:TextValue",
            "host_diet": "nmdc:TextValue",
            "host_genotype": "nmdc:TextValue",
            "host_life_stage": "nmdc:TextValue",
            "perturbation": "nmdc:TextValue",
            "source_mat_id": "nmdc:TextValue",
            "experimental_factor": "nmdc:ControlledTermValue",
            "samp_size": "nmdc:QuantityValue",
            "abs_air_humidity": "nmdc:QuantityValue",
            "avg_temp": "nmdc:QuantityValue",
            "fertilizer_regm": "nmdc:TextValue",
            "host_dry_mass": "nmdc:QuantityValue",
            "host_height": "nmdc:QuantityValue",
            "humidity": "nmdc:QuantityValue",
            "photon_flux": "nmdc:QuantityValue",
            "solar_irradiance": "nmdc:QuantityValue",
            "tot_carb": "nmdc:QuantityValue",
            "wind_direction": "nmdc:TextValue",
            "wind_speed": "nmdc:QuantityValue",
            "ammonium": "nmdc:QuantityValue",
            "diss_oxygen": "nmdc:QuantityValue",
            "chlorophyll": "nmdc:QuantityValue",
            "diss_inorg_nitro": "nmdc:QuantityValue",
            "soluble_react_phosp": "nmdc:QuantityValue",
            "sodium": "nmdc:QuantityValue",
            "sulfate": "nmdc:QuantityValue",
            "diss_inorg_carb": "nmdc:QuantityValue",
            "diss_org_carb": "nmdc:QuantityValue",
            "chloride": "nmdc:QuantityValue",
            "diss_iron": "nmdc:QuantityValue",
            "associated_dois": "nmdc:Doi",
            "has_credit_associations": "prov:Association",
            "principal_investigator": "nmdc:PersonValue",
            "study_image": "nmdc:ImageValue",
            "input_mass": "nmdc:QuantityValue",
            "quality_control_report": "nmdc:QualityControlReport"
            }

        # view = SchemaView("src/schema/nmdc.yaml")

        # # Get list of all classes that are used as ranges for slots (that are applicable to this migration)
        # value_classes = self.view.class_children("AttributeValue")
        # value_classes.extend(["ControlledIdentifiedTermValue", "Doi", "QualityControlReport"])
        #
        # # create a dictionary of inlined class uris
        # value_class_uris = {}
        # for value_class in value_classes:
        #     uri = self.view.get_class(value_class).class_uri
        #     value_class_uris[value_class] = uri
        #
        # # create dictionary of slots and their range's associated class_uris
        # slots_with_inlined_classes = {}
        # for slot_name, slot_def in self.view.all_slots().items():
        #     if slot_def.range in value_class_uris:
        #         slots_with_inlined_classes[slot_name] = value_class_uris[slot_def.range]

        # types_with_inlined_classes = ["nmdc:Biosample", "nmdc:Study", "nmdc:Extraction"]
        # Add the type slot to any inlined classes in the biosample_set
        for slot, uri in inlined_slots.items():
            self.add_type_to_inlined_classes(document, slot, uri)

        return document
