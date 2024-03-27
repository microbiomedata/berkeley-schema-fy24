var workflowActivitySets = ["mags_activity_set","metagenome_assembly_set", "metagenome_annotation_set", "metabolomics_analysis_activity_set",
"metaproteomics_analysis_activity_set", "metatranscriptome_activity_set", "nom_analysis_activity_set"];

var results = [];

workflowActivitySets.forEach(function(activitySet) {
    var pipeline = [
        {
            $unwind: "$was_informed_by"
        },
        {
            $lookup: {
                from: "omics_processing_set",
                localField: "was_informed_by",
                foreignField: "id",
                as: "output_docs"
            }
        },
        {
            $match: {
                output_docs: { $eq: [] }
            }
        },
        {
            $project: {
                _id: 1,
                has_output: 1
            }
        }
    ];

    var activityResults = db[activitySet].aggregate(pipeline).toArray();
    results.push({ activitySet: activitySet, activityResults: activityResults });
});

printjson(results);
