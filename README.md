
```
sam local generate-event http post --body '{"key1":"value1", "key2":"value2"}' --headers '{"Content-Type":"application/json"}' --path "/kakao" > event.json
```