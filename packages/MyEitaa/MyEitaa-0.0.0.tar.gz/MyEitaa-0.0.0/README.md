# Example Package

```
from MyEitaa import CleintEitaa as eitaa

apiKey : str = ""

app = eitaa(apiKey)

Data = app.sendMessage(message="hi", chatID = "1234" )

print(Data)

```