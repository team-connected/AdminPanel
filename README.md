# AdminPanel
## Docker Deploy
```docker run --name adminpanel -d -e apiUrl="http://umc-api.maartenmol.nl:5000" -p 8080:8080 team-connected/adminpanel```

### Environment Flags
| Flag | Description |
| ------------- | ------------- |
| api_url | URL to the API Cluster |