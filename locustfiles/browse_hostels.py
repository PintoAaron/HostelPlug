from random import randint
from locust import HttpUser, task, between



class BrowseHostels(HttpUser):
    wait_time = between(1,5)
    
    @task(4)
    def browse_hostels(self):
        self.client.get("/api/v1/hostels",name = "/api/v1/hostels")
        
    
    @task(2)
    def browse_hostel(self):
        hosteL_id = randint(1,32)
        self.client.get(f"/api/v1/hostels/{hosteL_id}",name = f"/api/v1/hostels/:id")
        
    
    @task(6)
    def browse_rooms(self):
        hostel_id = randint(1,32)
        self.client.get(f"/api/v1/hostels/{hostel_id}/rooms",name = f"/api/v1/hostels/:id/rooms")
        
    
    @task(3)
    def browse_room(self):
        hostel_id = randint(1,32)
        room_id = randint(1,14)
        self.client.get(f"/api/v1/hostels/{hostel_id}/rooms/{room_id}",name = f"/api/v1/hostels/:id/rooms/:id")
        
        
    
    @task(4)
    def browse_reviews(self):
        hostel_id = randint(1,32)
        self.client.get(f"/api/v1/hostels/{hostel_id}/reviews",name = f"/api/v1/hostels/:id/reviews")
        
    
    
    @task(2)
    def browse_review(self):
        hostel_id = randint(1,32)
        review_id = randint(1,15)
        self.client.get(f"/api/v1/hostels/{hostel_id}/reviews/{review_id}",name = f"/api/v1/hostels/:id/reviews/:id")
        
    
    
    @task(1)
    def add_a_review(self):
        hostel_id = randint(1,6)
        review = {
            "hostel":hostel_id,
            "rating":randint(1,5),
            "review":"Good hostel"
        }
        self.client.post(f"/api/v1/hostels/{hostel_id}/reviews",json = review,name = f"/api/v1/hostels/:id/reviews")
        
    
    
    @task(6)
    def browse_hostel_images(self):
        hostel_id = randint(1,32)
        self.client.get(f"/api/v1/hostels/{hostel_id}/images",name = f"/api/v1/hostels/:id/images")
        
    
    
    @task(3)
    def browse_hostel_image(self):
        hostel_id = randint(1,32)
        image_id = randint(1,10)
        self.client.get(f"/api/v1/hostels/{hostel_id}/images/{image_id}",name = f"/api/v1/hostels/:id/images/:id")