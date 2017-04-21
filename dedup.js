var collection = "semeval"
var duplicateField = "text"

var duplicates = [];

db.runCommand(
  {aggregate: collection,
    pipeline: [
      { $group: { _id: { text: "$" + duplicateField }, dups: { "$addToSet": "$_id" }, count: { "$sum": 1 } }},
      { $match: { count: { "$gt": 1 }}}
    ],
    allowDiskUse: true }
)
.result
.forEach(function(doc) {
    doc.dups.shift();
    doc.dups.forEach(function(dupId){ duplicates.push(dupId); })
})
printjson(duplicates); //optional print the list of duplicates to be removed

db.semeval.remove({_id:{$in:duplicates}});
