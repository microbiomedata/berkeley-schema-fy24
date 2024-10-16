# Merging the Berkeley schema into the NMDC schema

_Corresponding to a jump from major version 10 to 11_

This major refactoring increases the number of **classes** in the schema from 70 to 75, but decreases the number of root
classes from 19 to 17 due to better organization.

| Removed legacy class                | New/Replacement class from Berkeley schema | Selected legacy parents   |
|-------------------------------------|--------------------------------------------|---------------------------|
| Activity                            |                                            |                           |
| AnalyticalSample                    |                                            |                           |
| BiosampleProcessing                 |                                            |                           |
| BooleanValue                        |                                            | AttributeValue            |
| IntegerValue                        |                                            | AttributeValue            |
| MagsAnalysisActivity                | MagsAnalysis                               | WorkflowExecutionActivity |
| MetaboliteQuantification            | MetaboliteIdentification                   |                           |
| MetabolomicsAnalysisActivity        | MetabolomicsAnalysis                       | WorkflowExecutionActivity |
| MetagenomeAnnotationActivity        | MetagenomeAnnotation                       | WorkflowExecutionActivity |
| MetagenomeSequencingActivity        | MetagenomeSequencing                       | WorkflowExecutionActivity |
| MetaproteomicsAnalysisActivity      | MetaproteomicsAnalysis                     | WorkflowExecutionActivity |
| MetatranscriptomeAnnotationActivity | MetatranscriptomeAnnotation                | WorkflowExecutionActivity |
| NomAnalysisActivity                 | NomAnalysis                                | WorkflowExecutionActivity |
| OmicsProcessing                     | DataGeneration                             |                           |
| Reaction                            |                                            |                           |
| ReactionParticipant                 |                                            |                           |
| ReadBasedTaxonomyAnalysisActivity   | ReadBasedTaxonomyAnalysis                  | WorkflowExecutionActivity |
| ReadQcAnalysisActivity              | ReadQcAnalysis                             | WorkflowExecutionActivity |
| Solution                            |                                            |                           |
| SolutionComponent                   |                                            |                           |
| UrlValue                            |                                            | AttributeValue            |
| WorkflowExecutionActivity           |                                            |                           |
|                                     | CalibrationInformation                     |                           |
|                                     | ChemicalConversionProcess                  |                           |
|                                     | ChromatographyConfiguration                |                           |
|                                     | Configuration                              |                           |
|                                     | DissolvingProcess                          |                           |
|                                     | InformationObject                          |                           |
|                                     | Instrument                                 |                           |
|                                     | MassSpectrometry                           |                           |
|                                     | MassSpectrometryConfiguration              |                           |
|                                     | MaterialProcessing                         |                           |
|                                     | MobilePhaseSegment                         |                           |
|                                     | NucleotideSequencing                       |                           |
|                                     | PortionOfSubstance                         |                           |
|                                     | ProtocolExecution                          |                           |
|                                     | StorageProcess                             |                           |
|                                     | WorkflowExecution                          |                           |

For example, the `MetagenomeAnnotationActivity` class used to be located in the hierarchy
`Activity.WorkFlowExecutionActivity`, but now it and 11 similar classes are located in
`NamedThing.PlannedProcess.WorkflowExecution`. The word `Activity`, inherited from the Provenance Ontology, has largely
been removed from the schema, as `PlannedProcess` from the Ontology of Biomedical Investigations now plays a more
important organizational role.

## v10.9.1

![Activity.png](Activity.png)

`ProtocolExecution` has been added as a `PlannedProcess` for aggregating other processes together when they follow the
same `Protocol`.

![ProtocolExecution.png](ProtocolExecution.png)

Several other kinds of processual classes were also migrated into the `NamedThing.PlannedProcess`, with or without
renaming or other refactoring. For example, the fairly vague root class `OmicsProcessing` is now
`NamedThing.PlannedProcess.DataGeneration`, which now has the following subclasses:

- `MassSpectrometry`
- `NucleotideSequencing`

The legacy `BiosampleProcessing` class (including `Pooling`, `LibraryPreparation`) and some classes that were previously
direct subclasses of `PlannedProcess` (`Extraction`, `SubSamplingProcess`, `MixingProcess`, `FiltrationProcess`,
`ChromatographicSeparationProcess`) have been re-rooted into a new `MaterialProcessing` class.

`DissolvingProcess` and `ChemicalConversionProcess` are new subclasses of `MaterialProcessing` as of v11.

## v11.0.1

![MaterialProcessing.png](MaterialProcessing.png)

`StorageProcess` has been added as a new  `PlannedProcess` but is not considered `MaterialProcessing` because it does
not intrinsically create new/modified samples.

Terms that implied quantification like `MetaboliteQuantification` have been renamed to reemphasize the more fundamental
activity of identifying, thus `MetaboliteIdentification`

A `CalibrationInformation` class and two `Configuration` classes have been added in support of chromatographic
separations and mass spectrometry analyses. These are subclasses of the new `InformationObject`, which has also become
the parent of `DataObject`, which used to be a direct subclass of `NamedThing`.

## v11.0.1

![InformationObject.png](InformationObject.png)

## v11.0.1

![Configuration.png](Configuration.png)

Solution-centric modelling for laboratory processes was also replaced with substance-centric modelling

### Removed:

- `Solution`
- `SolutionComponent`

### Added:

- `PortionOfSubstance`
- `MobilePhaseSegment`

## v11.0.1

![PortionOfSubstance.png](PortionOfSubstance.png)

## v11.0.1

![MobilePhaseSegment.png](MobilePhaseSegment.png)

The Berkeley schema retains the `AttributeValue` hierarchy but eliminates classes like `IntegerValue`, and `UrlValue`
whose only advantages over a values of integer or string types were never-used provenance slots.

## v10.9.0

![AttributeValue10.png](AttributeValue10.png)

## v11.0.1

![AttributeValue11.png](AttributeValue11.png)

Classes related to metabolic reactions that a cell could carry out, based on some functionality in its genome, have been
removed, due to potential confusion with reactions that an experimenter might carry out in order to amke a sample
suitable for analysis.

### Removed:

- `Reaction`
- `ReactionParticipant`

### Added

- `ChemicalConversionProcess`

A very general `Instrument` class was added as a subclass of `MaterialEntity` , but without any subclasses. Knowledge
about instruments is captured directly in NMDC's MongoDB. The instances are normalized by populating their `vendor` slot
with a value from the `InstrumentVendorEnum` and by populating the `model` slot with a value from the
`InstrumentModelEnum`. Mappings between these NMDC vocabularies and vocabularies from collaborators like NCBI and GOLD
are saved in various repos like nmdc-schema and nmdc-runtime.

`AnalyticalSample` was removed from the `MaterialEntity` hierarchy, as NMDC does not wish to imply that certain samples
could be used for analyses or that other could not be used for analyses, or even that some samples a locked into an
analytical path, such that they could not be subject to any more `MaterialProcessing`.

----

The number of **slots** in the schema remains 872 after the Berkeley merger, although there are 44 slots that have been
retired from the legacy schema and 44 that were added in the switch from v10 to v11.

Many of the slot changes can be understood by looking at the Python data migration code in `nmdc_schema/migrators`

A major explanation for the slot differences is the adoption of a _polymorphic_  (ie multi-shaped) _model_  for slots in
the `Database` class, which corresponds to polymorphic collections in the v11-compliant MongoDB. In the legacy model,
the range for each of the `Database` slots was intended to be one class, with no provision for class hierarchy. In the
new model, the range for each slot is still specified as a single class, but the slots can collect instances of that
named class, plus the instances of any subclass of the class in the slots' range.

### Slots removed from `Database`

* extraction_set
* library_preparation_set
* mags_activity_set
* metabolomics_analysis_activity_set
* metagenome_annotation_activity_set
* metagenome_assembly_set
* metagenome_sequencing_activity_set
* metaproteomics_analysis_activity_set
* metatranscriptome_annotation_set
* metatranscriptome_assembly_set
* metatranscriptome_expression_analysis_set
* nom_analysis_activity_set
* omics_processing_set
* planned_process_set
* pooling_set
* read_based_taxonomy_analysis_activity_set
* read_qc_analysis_activity_set

### Slots added to `Database`

* calibration_set
* chemical_entity_set
* chromatographic_category
* configuration_set
* data_generation_set
* instrument_set
* material_processing_set
* protocol_execution_set
* storage_process_set
* workflow_execution_set

So now, instances of `MetaproteomicsAnalysis`, `MetatranscriptomeAnnotation` and `NomAnalysis` are all collected (or
aggregated) in `workflow_execution_set`.

These polymorphic collection are enabled by a significant modeling change in v11 of the schema: a strict requirement
that, within any represetnation of schema-compliant data, that all instances of all classes declare their own `type`.
Furthermore, the values in the `type` slot must be the `class_uri` of the instantiated class. That, in turn, means that
all classes must now declare a `class_uri` and that the `type` slots must be associated with each class. This is
enforced with the following Python tests:

* test_all_classes_assert_a_class_uri.py
* test_all_classes_can_use_type_slot.py

Note that classes should not re-associate themselves with any slot that they inherit form a superclass. For example, the
class definition for `Study`. This no-reasserting rule is tested with `test_inherited_slots_not_reiterated.py`

Also note that the legacy v10 schema did include a `type` slot, but it was used very inconsistently. v10 also ahd a
similar `designated_class` slot which ahs been retired.

The following slots were removed as a consequence of removing the `Reaction` class and beginning the process of
deprecating the `Pathway` class:

* chemical
* direction
* has_part
* has_participants
* is_balanced
* is_diastereoselective
* is_fully_characterized
* is_stereo
* is_transport
* left_participants
* right_participants
* smarts_string
* stoichiometry

`compound` and `has_solution_components` were removed as a consequence of removing the `Solution` class.

The string-typed `instrument_name` and `used` were removed due to refactoring around the new `Instrument` class and the
`instrument_used` slot, which is associated with numerous `PlannedProcess` subclasses.

The following have been removed from the `Extraction` class. _more details required_

* extractant
* extraction_method
* extraction_target

The string-typed `relevant_protocols` slot has been replaced with the `protocol_link` slot, which uses the `Protocol`
class as its range.

The string-typed `has_raw_value' has been replaced with `analyte_category`, which has an enumerated range:

* metagenome
* metatranscriptome
* metaproteome
* metabolome
* lipidome
* nom

In keeping with the focus on identification rather that quantification, `has_metabolite_quantifications` has been
replaced with `has_metabolite_identifications` and `metabolite_quantified` has been replaced with
`metabolite_identified`

`alternate_emails` and `keywords` were removed due to lack of use.

The `part_of` slots has been replaced in many cases with more specific slots. For example, Biosample now has an
`associated_studies` relationship with `Study`.

The NMDC schema has always imported many slots from the MIxS standard, and has generally associated them with the
`Biosmaple` class. In schema v11, several of those have been de-associated with Biosample as they are't really attributes of Biosamples

* chimera_check
* nucl_acid_amp
* nucl_acid_ext
* pcr_cond
* pcr_primers
* pool_dna_extracts
* samp_vol_we_dna_ext
* seq_meth
* seq_quality_check
* target_gene
* target_subfragment

Some, but not all of those slots were re-associated with `Extraction`, `LibraryPreparation` or `NucleotideSequencing`

`has_process_parts` has been added to capture the relationship between a `ProtocolExecution` and the Process instances
that were carried out with the intention of completing a specified protocol under specified circumstances.

The following slots have been added in support of the new `CalibrationInformation` and `Configuration` modelling for
`MassSpectrometry`. The new schema's increased use of boolean and enumerated ranges (as opposed to
open-ended string ranges) is nicely illustrated by these slots.

* calibration_object
* calibration_standard
* calibration_target
* internal_calibration
* has_chromatography_configuration
* has_mass_spectrometry_configuration

The following slots have been added, specifically on `MassSpectrometryConfiguration`, so that a small number of
`MassSpectrometryConfiguration` instances can be reused to describe

* mass_analyzers
* mass_spectrometry_acquisition_strategy
* mass_spectrum_collection_modes
* ionization_source
* polarity_mode
* resolution_categories

These new slots are examplars of the increased emphasis on enumeration ranges (and the avoidance of the word 'type' in
slot names other than `type`)

- analyte_category
- chemical_conversion_category
- chromatographic_category _applicable to `ChromatographyConfiguration`     and `ChromatographicSeparationProcess` ?_
- data_category
- direct_infusion_category
- eluent_introduction_category
- feature_category
- protocol_execution_category

The following new slots support the change from solution-based modeling to substance-based modelling:

* substance_role
* substances_used
* substances_volume
* source_concentration
* final_concentration
* sample_state_information

The `ChemicalEntity` class has been refactored for nmdc-schema v11, and is likely to undergo additional changes in later
2024 and 2025. For now, a `known_as` slot has been added to allow for flexibility in `PortionOfSubstance` and retain
precision in `ChemicalEntity`

`extraction_targets` was added to `Extraction`, `sampled_portion` was added to `SubSamplingProcess` and
`jgi_portal_analysis_project_identifiers`



----

v10 of the schema provided 168 example data files. v11 has increased that to 224, providing better testing coverage of
the schema via the `run-linkml-example` phase of `make test`

v11 is also more thorough in annotating abstract classes, with 11, compared to 7 in v10. That includes a new `abstract`
annotation for `AttributeValue`,  `MaterialProcessing` (which essentially replaces `BiosampleProcessing`) and
`DataGeneration` (which essentially replaces `OmicsProcessing`)

----

Running the whole schema though a tool like deepdiff can be overwhelming, but extracting a single class (or induced
class?) from two version of the schema and then deep diffing them like this can be enlightening

```make
pre_schema.yaml:
	poetry run python -c 'from linkml_runtime.utils.schemaview import SchemaView; \
	from linkml_runtime.dumpers import yaml_dumper; \
	schema_url = "https://raw.githubusercontent.com/microbiomedata/nmdc-schema/refs/tags/v10.9.1/src/schema/nmdc.yaml"; \
	sv = SchemaView(schema_url, merge_imports=True); \
	yaml_dumper.dump(sv.schema, "pre_schema.yaml")'

berkeley_schema.yaml:
	poetry run python -c 'from linkml_runtime.utils.schemaview import SchemaView; \
	from linkml_runtime.dumpers import yaml_dumper; \
	schema_url = "https://raw.githubusercontent.com/microbiomedata/nmdc-schema/refs/tags/v11.0.1/src/schema/nmdc.yaml"; \
	sv = SchemaView(schema_url, merge_imports=True); \
	yaml_dumper.dump(sv.schema, "berkeley_schema.yaml")'

pre_study.yaml: pre_schema.yaml
	yq '.classes.Study' $< | cat > $@

berkeley_study.yaml: berkeley_schema.yaml
	yq '.classes.Study' $< | cat > $@

pre_vs_berkeley_study.yaml: pre_study.yaml berkeley_study.yaml
	poetry run deep diff --ignore-order $^ | yq -P | cat > $@
```

```yaml
dictionary_item_added:
  - root['class_uri']
  - root['slot_usage']['protocol_link']
values_changed:
  root['from_schema']:
    new_value: https://w3id.org/nmdc/basic_classes
    old_value: https://w3id.org/nmdc/nmdc
iterable_item_added:
  root['slots'][24]: protocol_link
iterable_item_removed:
  root['slots'][3]: id
  root['slots'][4]: alternative_identifiers
  root['slots'][9]: description
  root['slots'][26]: relevant_protocols
  root['slots'][30]: type
```

This reveals that the `class_uri` and `protocol_link` slots were added as described above. The `from_schema` values
reveals the fact that v11 splits the elements of the schema into different YAML source files. The large number of files
was intended to make it easier to debug build errors, but it has been difficult to split the contents into files that
have a consistent domain or topic.

The diff also shows the removal of the `id`, `alternative_identifiers`, `description`, `relevant_protocols` and `type`
slots, which might be counter-intuitive, until one considers that all of those slots are inherited from `Study`'s
parent, `NamedThing` and that schema v11 forbids re-asserting slots that are inherited from a superclass.

Expansions for the following prefixes were added:
- NCBI _needs better modeling for NCBI taxonomy identifiers_
- SO
- jgi.analysis
- MISO

The following enumerations were removed:
- CompoundEnum
- DeviceEnum

`processing_institution_enum` was renamed to `ProcessingInstitutionEnum`

And the following enumerations were added:
- AnalyteCategoryEnum
- CalibrationStandardEnum
- CalibrationTargetEnum
- ChemicalConversionCategoryEnum
- ChromatographicCategoryEnum
- DataCategoryEnum
- DirectInfusionEnum
- EluentIntroductionCategoryEnum
- ExecutionResourceEnum
- IonizationSourceEnum
- MassAnalyzerEnum
- MassSpectrometryAcquisitionStrategyEnum
- MassSpectrumCollectionModeEnum
- PolarityModeEnum
- ProcessingInstitutionEnum
- ProtocolCategoryEnum
- ResolutionCategoryEnum
- SamplePortionEnum
- SampleStateEnum
- SubstanceRoleEnum

----

id patterns... to what degree did these change between versions?

