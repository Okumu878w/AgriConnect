🌻 AgriConnect (Django)
Bridging the gap between farmers, buyers, and agricultural experts.

AgriConnect is a comprehensive digital platform built with Django designed to empower agricultural producers. It creates a direct link between farmers and buyers to eliminate supply chain inefficiencies and provides a vital Expert Advisory service to help farmers diagnose crop diseases quickly.

Problem Statement
The current agricultural landscape faces significant challenges:

Low Farmer Margins: Reliance on middlemen reduces the profit for producers.

Crop Health Risks: Farmers lack immediate access to certified agronomists when crops show signs of disease.

Market Inefficiency: Buyers lack a centralized platform to find specific crops in specific locations.

Solution
AgriConnect offers a centralized Django-based web platform with three core pillars:

Direct Marketplace: A transparent catalog where farmers list produce and buyers connect directly via phone.

Seller Dashboard: A management interface for farmers to track their stock and pricing.

Expert Advisory: A paid consultation module where farmers upload photos of unhealthy crops to get diagnosis and advice from certified experts.

 Key Features
1. Marketplace (For Buyers & Sellers)
Visual Product Cards: Crops are displayed with high-quality images, pricing, and available stock.

Advanced Filtering: Search functionality allows users to find products by Name, Location (e.g., Kitale, Bungoma, Kericho), or Category.

Direct Connection: Integrated "Call" button on product cards allows buyers to contact farmers immediately via mobile.

Wishlist: "Save" functionality for buyers to track products they are interested in.

2. Seller Dashboard (For Farmers)
Inventory Management: A CRUD interface allowing farmers to:

Add Item: List new crops with category and price.

Edit/Delete: Update pricing or remove items that are out of stock.

View List: A clean tabular view of all current holdings.

Role-Based Access: Secure login ensures only the account owner can modify their inventory.

3.  Expert Advisory Module (New!)
Disease Diagnosis: A dedicated section for farmers to ask: "Crop looking unhealthy? Don't guess."

Consultation Workflow:

Request: User describes the problem (e.g., "Leaves turning yellow") and uploads a photo of the affected crop.

Payment: Integrated M-Pesa phone number field for consultation fees (KES 50/=).

Expert Analysis: Certified agronomists review the photo and description.

Resolution: Farmers receive specific advice (e.g., "Plant legumes such as beans...") and the ticket is marked as ✅ Solved.

History Tracking: Users can view a log of all past consultations, including payment status (Unpaid/Pending/Paid) and expert responses.

🛠 Tech Stack
Backend Framework: Django 4.x / 5.x

Language: Python 3.x

Database: SQLite (Development)

Frontend: Django Templates (DTL) + Bootstrap 5 (Responsive Design)

Integrations: M-Pesa (Simulated/Implemented for Advisory payments)







