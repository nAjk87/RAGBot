async def stream_generator(streamManager):
    try:
        async with streamManager as stream:
            async for event in stream:
                if event.event == "thread.message.delta":
                    for d in event.data.delta.content:
                        yield d.text.value
                if event.event == "thread.run.requires_action":
                    run_id = event.data.id  # Retrieve the run ID from the event data
                    async with stream.handle_requires_action(
                        event.data, run_id
                    ) as toolStream:
                        async for tooltext in toolStream.text_deltas:
                            yield tooltext

                yield ""
    except asyncio.TimeoutError:
        raise HTTPException(status_code=504, detail="Stream timed out")