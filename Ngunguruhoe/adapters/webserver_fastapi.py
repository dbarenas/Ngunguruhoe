from fastapi import FastAPI
from Ngunguruhoe.domain.models.alert import Alert
from Ngunguruhoe.domain.ports.alert_port import AlertPort

def create_app(alert_repo: AlertPort):
    app = FastAPI()

    @app.get("/latest-alert", response_model=Alert | None)
    async def latest_alert():
        return await alert_repo.get_latest_alert()

    return app
