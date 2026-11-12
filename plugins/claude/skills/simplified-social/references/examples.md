# Social payload examples

### Simple Queue Post

```
1. social_getSocialMediaAccounts({})
2. social_createSocialMediaPost({
     message: "Check out our new feature! 🚀",
     account_ids: ["123"],
     action: "add_to_queue",
     media: ["https://cdn.example.com/image.jpg"],
     additional: {
       instagram: { postType: { value: "post" }, channel: { value: "direct" } }
     }
   })
```

### Scheduled YouTube Short

```
1. social_getSocialMediaAccounts({})
2. social_createSocialMediaPost({
     message: "Quick tip: how to use our API",
     account_ids: ["456"],
     action: "schedule",
     date: "2027-06-10 14:00",
     media: ["https://cdn.example.com/video.mp4"],
     additional: {
       youtube: { postType: { value: "short" },
         post: { title: "API Quick Tip", privacyStatus: "public", selfDeclaredMadeForKids: "no" } }
     }
   })
```

### Post a freshly generated image

```
1. (generate-image skill) → asset_id "11111111-1111-4111-8111-111111111111"
2. social_getSocialMediaAccounts({})
3. social_createSocialMediaPost({
     message: "Meet the new drop 👟",
     account_ids: ["123"],
     action: "draft",
     media: ["11111111-1111-4111-8111-111111111111"],                       // asset UUID from generate-image
     additional: { instagram: { postType: { value: "post" }, channel: { value: "direct" } } }
   })
```

### Reddit draft

```
1. social_getSocialMediaAccounts({})
2. social_createSocialMediaPost({
     message: "What we learned from shipping our new workflow",
     account_ids: ["789"],
     action: "draft",
     additional: {
       reddit: {
         post: {
           targets: [{
             subreddit: "devtestsmp",
             title: "What we learned from shipping our new workflow",
             type: "self",
             flairId: null,
             flairText: null,
             nsfw: false,
             url: null
           }]
         }
       }
     }
   })
```

### Link in the first comment after 5 minutes

```
1. If not already approved unchanged, preview and obtain authorization for the main post and:
   first comment: "Read the full guide: https://example.com/guide"
   delay: 5 minutes after the post publishes
2. social_createSocialMediaPost({
     message: "We published a practical guide to better campaign reviews.",
     account_ids: ["123"],
     action: "schedule",
     date: "2027-06-10 14:00",
     comments: [{
       message: "Read the full guide: https://example.com/guide",
       delay: 300
     }]
   })
```

### Analytics: Account Overview

```
1. social_getSocialMediaAccounts({})
2. social_getSocialMediaAnalyticsAggregated({ account_id: 789, date_from: "2026-05-01", date_to: "2026-05-31" })
```

