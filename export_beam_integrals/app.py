from celery import Celery


app = Celery('export_beam_integrals')
app.config_from_object('export_beam_integrals.celeryconfig')


if __name__ == '__main__':
    app.start()
