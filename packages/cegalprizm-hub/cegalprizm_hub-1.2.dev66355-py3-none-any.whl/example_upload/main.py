from cegalprizm.hub import Hub

# Create a new Hub object
hub = Hub()

# Get a default hub Agent context
agent_context = hub.default_agent_ctx()

# Upload the file
res = agent_context.upload_file(src_path='./index.html', open_file_on_complete=True, overwrite=True)

print(res)