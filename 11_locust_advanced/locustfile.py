from locust import HttpUser, task, SequentialTaskSet, between
import random
import time

RESPONSE_TIME_LIMIT_MS = 3000.0


class PetShopWorkflow(SequentialTaskSet):
    # This task will always run FIRST because the TaskSet is Sequential
    @task
    def add_new_pet(self):
        # Create a unique name for our new pet
        pet_name = f"Fluffy-{random.randint(1, 10000)}"

        self.client.post("/pets", json={"name": pet_name, "category": "dog"})

    # # This task will always run SECOND
    # @task
    # def load_homepage(self):
    #     self.client.get("/")

    @task
    def load_homepage(self):
        # 1. Record the time *before* the request
        start_time = time.time()

        # 2. Make the request, but use 'catch_response=True'.
        # This tells Locust: "Don't automatically mark this as success/failure. I will do it myself."
        with self.client.get("/", catch_response=True) as response:
            # 3. Calculate the total response time in milliseconds
            response_time_ms = (time.time() - start_time) * 1000

            # 4. Implement our custom SLO logic
            if response_time_ms > RESPONSE_TIME_LIMIT_MS:
                # 5. MANUALLY fail the request
                response.failure(
                    f"Response time exceeded {RESPONSE_TIME_LIMIT_MS}ms: ({response_time_ms:.0f}ms)"
                )

            elif response.status_code != 200:
                # 6. Manually fail on bad status codes (just in case)
                response.failure(f"Got non-200 status code: {response.status_code}")

            else:
                # 7. MANUALLY mark it as a success
                response.success()


class PetShopUser(HttpUser):
    host = "http://127.0.0.1:5000"
    wait_time = between(0, 0)
    tasks = [PetShopWorkflow]
