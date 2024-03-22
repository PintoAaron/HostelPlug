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
        hostel_id = 30
        room_id = 15
        self.client.get(f"/api/v1/hostels/{hostel_id}/rooms/{room_id}",name = f"/api/v1/hostels/:id/rooms/:id")
        
        
    
    @task(4)
    def browse_reviews(self):
        hostel_id = randint(1,32)
        self.client.get(f"/api/v1/hostels/{hostel_id}/reviews",name = f"/api/v1/hostels/:id/reviews")
        
    
    
    @task(2)
    def browse_review(self):
        hostel_id = 30
        review_id = 16
        self.client.get(f"/api/v1/hostels/{hostel_id}/reviews/{review_id}",name = f"/api/v1/hostels/:id/reviews/:id")
        
        
    
    
    @task(6)
    def browse_hostel_images(self):
        hostel_id = 30
        self.client.get(f"/api/v1/hostels/{hostel_id}/images",name = f"/api/v1/hostels/:id/images")
        
    
    
    @task(3)
    def browse_hostel_image(self):
        hostel_id = 30
        image_id = 9
        self.client.get(f"/api/v1/hostels/{hostel_id}/images/{image_id}",name = f"/api/v1/hostels/:id/images/:id")