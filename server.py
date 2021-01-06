import logging
import asyncio
import aiocoap.resource as resource
import aiocoap
import modules.singIn as singIn
import modules.singUp as singUp
import modules.histUser as histUser

# Logging Setup
logging.basicConfig(level=logging.INFO)
logging.getLogger("coap-server").setLevel(logging.DEBUG)

def main():
    # Resource tree creation
    root = resource.Site()
    root.add_resource(['signup'], singUp.SignUp())
    root.add_resource(['signin'], singIn.SignIn())
    root.add_resource(['histuser'], histUser.HistoryUser())
    asyncio.Task(aiocoap.Context.create_server_context(root))
    asyncio.get_event_loop().run_forever()

if __name__ == "__main__":
    main()