from locust import HttpUser, task, between

class BuscadorUser(HttpUser):
    wait_time = between(1, 3)

    @task
    def abrir_home(self):
        self.client.get("/")  # home do Streamlit app

    @task
    def buscar_dados_externos(self):
        self.client.get("https://api.openalex.org/works?search=climate")
