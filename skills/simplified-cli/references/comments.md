# Comments through `smp api`

Comments use `content_type` and `object_pk`; they are generated in the `api` namespace. Resolve the task UUID and read existing comments before replying. Posting a comment requires the user's instruction to communicate it.

```bash
smp api:list-comments --content-type task --object-pk <task-uuid> --page 1
smp api:add-comment --content-type task --object-pk <task-uuid> --comment "Ready for review"
smp api:add-comment --content-type task --object-pk <task-uuid> --comment "Updated as requested" --parent <integer-comment-id>
```

`parent` is an integer comment ID from the response, not a task UUID. Retain the selected workspace/teamspace scope. Do not turn comments into an unsolicited notification or assume every resource type is supported; inspect current command help.
