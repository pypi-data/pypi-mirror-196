# py-Puii Library

# Installation
```bash
pip3 install -U py-Puii
```


# Usage
- Create folders named `plugins`, `addons`, `assistant` and `resources`.   
- Add your plugins in the `plugins` folder and others accordingly.   
- Create a `.env` file with following mandatory Environment Variables
   ```
   API_ID
   API_HASH
   SESSION
   REDIS_URI
   REDIS_PASSWORD
   ```
- Check
[`.env.sample`](https://github.com/AellyXD/Puii/blob/main/.env.sample) for more details.   
- Run `python3 -m pyPuii` to start the bot.   

## Creating plugins
 - ### To work everywhere

```python
@puii_cmd(
    pattern="start"
)   
async def _(e):   
    await e.eor("Puii Started!")   
```

- ### To work only in groups

```python
@puii_cmd(
    pattern="start",
    groups_only=True,
)   
async def _(e):   
    await eor(e, "Puii Started.")   
```

- ### Assistant Plugins 👇

```python
@asst_cmd("start")   
async def _(e):   
    await e.reply("Puii Started.")   
```
