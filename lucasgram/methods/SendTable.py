import matplotlib.pyplot as plt
import pandas as pd
import io

async def SendTable(self, chat_id, data, caption=None, message_thread_id: int = None):
    df = pd.DataFrame(data)

    fig, ax = plt.subplots()
    ax.axis('off')
    ax.axis('tight')
    ax.table(cellText=df.values, colLabels=df.columns, loc='center')

    # save the table as an image in memory
    buffer = io.BytesIO()
    plt.savefig(buffer, format='png')
    buffer.seek(0)

    await self.send_photo(chat_id=chat_id, photo=buffer, caption=caption, message_thread_id=message_thread_id)
