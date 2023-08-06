import gradio as gr

from .pipeline import Pipeline


def app(task, model_dir, device=-1, batch_size=1, examples=[]):
    pipe = Pipeline(task, model_dir, device=device, batch_size=batch_size)

    def predict(text):
        return str(pipe(text))

    app = gr.Interface(
        fn=predict,
        inputs='text',
        outputs='text',
        examples=[examples]
    )

    app.launch(share=True)
