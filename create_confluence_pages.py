
import os
import sys
import base64
import json
import urllib.request
import urllib.error

# Force UTF-8 output on Windows
sys.stdout.reconfigure(encoding='utf-8')

BASE_URL = "https://mrithighasai.atlassian.net/wiki"
SPACE_KEY = "~712020479256762aae49f6b18ba62c2412fa71"
EMAIL = os.environ["JIRA_EMAIL"]
PAT = os.environ["JIRA_PAT"]

token = base64.b64encode(f"{EMAIL}:{PAT}".encode()).decode()
HEADERS = {
    "Authorization": f"Basic {token}",
    "Content-Type": "application/json",
    "Accept": "application/json",
}

def find_page_by_title(title):
    """Return page ID if a page with this title already exists in the space, else None."""
    import urllib.parse
    params = urllib.parse.urlencode({"title": title, "spaceKey": SPACE_KEY, "type": "page"})
    req = urllib.request.Request(
        f"{BASE_URL}/rest/api/content?{params}",
        headers=HEADERS,
        method="GET"
    )
    try:
        with urllib.request.urlopen(req) as resp:
            result = json.loads(resp.read())
            results = result.get("results", [])
            if results:
                return results[0]["id"]
    except Exception:
        pass
    return None


def create_page(title, body, parent_id=None):
    payload = {
        "type": "page",
        "title": title,
        "space": {"key": SPACE_KEY},
        "body": {
            "storage": {
                "value": body,
                "representation": "storage"
            }
        }
    }
    if parent_id:
        payload["ancestors"] = [{"id": parent_id}]

    data = json.dumps(payload).encode("utf-8")
    req = urllib.request.Request(
        f"{BASE_URL}/rest/api/content",
        data=data,
        headers=HEADERS,
        method="POST"
    )
    try:
        with urllib.request.urlopen(req) as resp:
            result = json.loads(resp.read())
            page_id = result["id"]
            print(f"  Created: '{title}' -> ID={page_id}")
            return page_id
    except urllib.error.HTTPError as e:
        body_err = e.read().decode()
        if e.code == 400 and "already exists" in body_err:
            existing_id = find_page_by_title(title)
            if existing_id:
                print(f"  Already exists: '{title}' -> ID={existing_id} (skipped)")
                return existing_id
        print(f"  ERROR creating '{title}': HTTP {e.code} -- {body_err}")
        raise

# ── Page content ──────────────────────────────────────────────────────────────

PAGE_CONTENT = {}

PAGE_CONTENT["GemstoneWorld — Engineering Hub"] = """
<ac:structured-macro ac:name="info">
  <ac:parameter ac:name="title">About This Space</ac:parameter>
  <ac:rich-text-body>
    <p>This space contains all technical documentation for the GemstoneWorld jewellery e-commerce application. Use the page tree on the left to navigate to specific services, sequence diagrams, data models, and testing notes.</p>
  </ac:rich-text-body>
</ac:structured-macro>
<h2>Quick Links</h2>
<table>
  <tbody>
    <tr><th>Repository</th><th>Purpose</th><th>Link</th></tr>
    <tr><td>gemstoneworld</td><td>React Frontend</td><td><a href="https://github.com/Mrithigha/gemstoneworld">GitHub</a></td></tr>
    <tr><td>gemstoneworld-auth-service</td><td>Auth microservice</td><td><a href="https://github.com/Mrithigha/gemstoneworld-auth-service">GitHub</a></td></tr>
    <tr><td>gemstoneworld-products-service</td><td>Products microservice</td><td><a href="https://github.com/Mrithigha/gemstoneworld-products-service">GitHub</a></td></tr>
    <tr><td>gemstoneworld-cart-service</td><td>Cart microservice</td><td><a href="https://github.com/Mrithigha/gemstoneworld-cart-service">GitHub</a></td></tr>
    <tr><td>gemstoneworld-orders-service</td><td>Orders microservice</td><td><a href="https://github.com/Mrithigha/gemstoneworld-orders-service">GitHub</a></td></tr>
  </tbody>
</table>
<h2>Service Ports</h2>
<table>
  <tbody>
    <tr><th>Service</th><th>Port</th><th>Base URL</th></tr>
    <tr><td>Frontend</td><td>5173</td><td>http://localhost:5173</td></tr>
    <tr><td>Auth Service</td><td>3001</td><td>http://localhost:3001/api/auth</td></tr>
    <tr><td>Products Service</td><td>3002</td><td>http://localhost:3002/api</td></tr>
    <tr><td>Cart Service</td><td>3003</td><td>http://localhost:3003/api</td></tr>
    <tr><td>Orders Service</td><td>3004</td><td>http://localhost:3004/api</td></tr>
  </tbody>
</table>
"""

PAGE_CONTENT["1. Application Overview"] = """
<h2>About GemstoneWorld</h2>
<p>GemstoneWorld is a full-stack e-commerce application for buying fine jewellery online. It is built as a microservices architecture with a React frontend and four independent Java Spring Boot backend services, each backed by a file-based H2 database.</p>
<p><strong>Business domain:</strong> Online retail of jewellery across four categories &mdash; Gold, Silver, Diamond, and Imitation.</p>
<h2>Technology Stack</h2>
<table>
  <tbody>
    <tr><th>Layer</th><th>Technology</th><th>Version</th></tr>
    <tr><td>Frontend</td><td>React + Vite</td><td>React 18</td></tr>
    <tr><td>Routing</td><td>React Router</td><td>v6</td></tr>
    <tr><td>HTTP Client</td><td>Axios</td><td>&mdash;</td></tr>
    <tr><td>Backend</td><td>Java + Spring Boot</td><td>Java 17, Spring Boot 3.2</td></tr>
    <tr><td>ORM</td><td>Spring Data JPA</td><td>&mdash;</td></tr>
    <tr><td>Database</td><td>H2 file-based persistent</td><td>&mdash;</td></tr>
    <tr><td>Authentication</td><td>JWT + BCrypt</td><td>jjwt 0.12.3</td></tr>
    <tr><td>Build Tool</td><td>Maven</td><td>3.8+</td></tr>
  </tbody>
</table>
<h2>Key User Journeys</h2>
<table>
  <tbody>
    <tr><th>#</th><th>Journey</th><th>Entry Point</th><th>Auth Required</th></tr>
    <tr><td>1</td><td>Register a new account</td><td>/register</td><td>No</td></tr>
    <tr><td>2</td><td>Log in to existing account</td><td>/login</td><td>No</td></tr>
    <tr><td>3</td><td>Browse and search jewellery catalogue</td><td>/products</td><td>No</td></tr>
    <tr><td>4</td><td>View product detail</td><td>/products/:id</td><td>No</td></tr>
    <tr><td>5</td><td>Add product to cart</td><td>/products/:id</td><td>Yes &mdash; redirects to login</td></tr>
    <tr><td>6</td><td>View and manage cart</td><td>/cart</td><td>View: No &mdash; Manage: Yes</td></tr>
    <tr><td>7</td><td>Checkout and place order</td><td>/checkout</td><td>Yes &mdash; protected route</td></tr>
    <tr><td>8</td><td>View order history</td><td>/orders</td><td>Yes &mdash; protected route</td></tr>
  </tbody>
</table>
<h2>Catalogue Summary</h2>
<table>
  <tbody>
    <tr><th>Category</th><th>Product Count</th><th>Price Range (INR)</th></tr>
    <tr><td>Gold</td><td>11</td><td>8,800 &ndash; 68,500</td></tr>
    <tr><td>Silver</td><td>10</td><td>680 &ndash; 5,200</td></tr>
    <tr><td>Diamond</td><td>10</td><td>42,000 &ndash; 2,45,000</td></tr>
    <tr><td>Imitation</td><td>11</td><td>250 &ndash; 1,850</td></tr>
    <tr><td><strong>Total</strong></td><td><strong>42</strong></td><td>&mdash;</td></tr>
  </tbody>
</table>
<p><strong>Product types:</strong> necklaces, earrings, rings, bracelets, pendants, chains</p>
"""

PAGE_CONTENT["2. High Level Design"] = """
<h2>Architecture Overview</h2>
<p>GemstoneWorld follows a microservices architecture. The React frontend communicates directly with each backend service over HTTP using Axios. There is no API gateway &mdash; the frontend holds the base URLs for each service. Each service has its own isolated H2 file-based database.</p>
<h2>Component Diagram</h2>
<ac:structured-macro ac:name="code">
  <ac:parameter ac:name="language">text</ac:parameter>
  <ac:plain-text-body><![CDATA[
+--------------------------------------------------------------+
|                  React Frontend (Vite)                        |
|                  http://localhost:5173                        |
|                                                              |
|  /              -> Home                                      |
|  /products      -> Product Listing                           |
|  /products/:id  -> Product Detail                            |
|  /cart          -> Shopping Cart                             |
|  /checkout      -> Checkout (protected)                      |
|  /orders        -> Order History (protected)                 |
|  /login         -> Login                                     |
|  /register      -> Register                                  |
+------------+-------------------------------------------------+
             | HTTP / Axios
   +---------v--------------------------------------------------+
   |                   Backend Services                         |
   |                                                            |
   |  auth-service      -> http://localhost:3001               |
   |  products-service  -> http://localhost:3002               |
   |  cart-service      -> http://localhost:3003               |
   |  orders-service    -> http://localhost:3004               |
   +---------+--------------------------------------------------+
             |
   +---------v--------------------------------------------------+
   |              H2 File-Based Databases                       |
   |                                                            |
   |  ./data/auth-db      (users table)                        |
   |  ./data/products-db  (products, product_sizes)            |
   |  ./data/cart-db      (cart_items table)                   |
   |  ./data/orders-db    (orders, order_items)                |
   +------------------------------------------------------------+
  ]]></ac:plain-text-body>
</ac:structured-macro>
<h2>Authentication Design</h2>
<p>Authentication uses stateless JWT tokens issued exclusively by the Auth Service. The Cart and Orders services validate tokens independently using a shared secret key &mdash; they do not call the Auth Service at runtime.</p>
<table>
  <tbody>
    <tr><th>Property</th><th>Value</th></tr>
    <tr><td>JWT shared secret</td><td>gsw-jwt-secret-key-for-gemstoneworld-application-2024-shared</td></tr>
    <tr><td>Token expiry</td><td>7 days (604800000 ms)</td></tr>
    <tr><td>Password hashing</td><td>BCrypt</td></tr>
    <tr><td>Token storage (client)</td><td>localStorage</td></tr>
    <tr><td>CORS allowed origins</td><td>http://localhost:5173, http://localhost:4173</td></tr>
  </tbody>
</table>
<h2>Service Responsibilities</h2>
<table>
  <tbody>
    <tr><th>Service</th><th>Responsibility</th><th>Auth Required</th><th>Inter-service Calls</th></tr>
    <tr><td>Auth Service</td><td>User registration, login, token issuance, session validation</td><td>No (public endpoints)</td><td>None</td></tr>
    <tr><td>Products Service</td><td>Serve jewellery catalogue &mdash; read only, public</td><td>No</td><td>None</td></tr>
    <tr><td>Cart Service</td><td>Per-user cart management &mdash; add, update, remove, clear</td><td>Yes &mdash; JWT</td><td>None (validates JWT locally)</td></tr>
    <tr><td>Orders Service</td><td>Order placement and order history</td><td>Yes &mdash; JWT</td><td>None (validates JWT locally, does not call Cart)</td></tr>
    <tr><td>Frontend</td><td>UI, routing, state management, API orchestration</td><td>Context-dependent</td><td>Calls all four services directly</td></tr>
  </tbody>
</table>
<ac:structured-macro ac:name="warning">
  <ac:parameter ac:name="title">Important Design Note</ac:parameter>
  <ac:rich-text-body>
    <p>The Orders Service does NOT call the Cart Service. When an order is placed, the frontend sends the cart items snapshot directly to the Orders Service. Cart clearing after order placement is the frontend&apos;s responsibility &mdash; it calls DELETE /api/cart/clear after a successful order response.</p>
  </ac:rich-text-body>
</ac:structured-macro>
"""

PAGE_CONTENT["3. User Journey Sequence Diagrams"] = """
<p>This section contains step-by-step sequence diagrams for all key user journeys in GemstoneWorld. Each sub-page covers one journey showing the interaction between the user, React frontend, and backend services.</p>
<table>
  <tbody>
    <tr><th>Journey</th><th>Page</th></tr>
    <tr><td>Register and Login</td><td>3.1 Register and Login</td></tr>
    <tr><td>Browse and Search Products</td><td>3.2 Browse and Search Products</td></tr>
    <tr><td>Add to Cart</td><td>3.3 Add to Cart</td></tr>
    <tr><td>Checkout and Place Order</td><td>3.4 Checkout and Place Order</td></tr>
    <tr><td>View Order History</td><td>3.5 View Order History</td></tr>
  </tbody>
</table>
"""

PAGE_CONTENT["3.1 Register and Login"] = """
<h2>User Journey: Register a New Account</h2>
<ac:structured-macro ac:name="code">
  <ac:parameter ac:name="language">text</ac:parameter>
  <ac:plain-text-body><![CDATA[
User          React Frontend           Auth Service          localStorage
 |                   |                      |                      |
 |-- Navigate /register -->                 |                      |
 |                   |-- Render form -----> |                      |
 |-- Fill form ----> |                      |                      |
 |-- Submit -------> |                      |                      |
 |                   |-- POST /api/auth/register ----------------> |
 |                   |                      |-- Validate fields    |
 |                   |                      |-- Check email unique |
 |                   |                      |-- Hash password      |
 |                   |                      |-- Save user to DB    |
 |                   |                      |-- Issue JWT token    |
 |                   |<-- 200 { token, user } ------------------- |
 |                   |-- Store token + user --------------------> |
 |                   |-- Update AuthContext                        |
 |                   |-- Redirect to /                            |
 |<-- Home page ---- |                                            |

Error paths:
 |                   |<-- 400 { error: "Email already registered." }
 |                   |<-- 400 { error: "Password must be at least 6 characters." }
 |                   |-- Display error message inline             |
  ]]></ac:plain-text-body>
</ac:structured-macro>
<h2>User Journey: Login</h2>
<ac:structured-macro ac:name="code">
  <ac:parameter ac:name="language">text</ac:parameter>
  <ac:plain-text-body><![CDATA[
User          React Frontend           Auth Service          localStorage
 |                   |                      |                      |
 |-- Navigate /login ->                     |                      |
 |-- Fill email + password                  |                      |
 |-- Submit -------> |                      |                      |
 |                   |-- POST /api/auth/login ------------------>  |
 |                   |                      |-- Validate email     |
 |                   |                      |-- BCrypt compare     |
 |                   |                      |-- Issue JWT token    |
 |                   |<-- 200 { token, user } ----------------    |
 |                   |-- Store token + user --------------------> |
 |                   |-- Update AuthContext                        |
 |                   |-- Redirect to /                            |
 |<-- Home page ---- |                                            |

Error paths:
 |                   |<-- 401 { error: "Invalid email or password." }
 |                   |-- Display error message inline             |
  ]]></ac:plain-text-body>
</ac:structured-macro>
<h2>Session Restore on Page Load</h2>
<ac:structured-macro ac:name="code">
  <ac:parameter ac:name="language">text</ac:parameter>
  <ac:plain-text-body><![CDATA[
Browser Load     React Frontend           Auth Service          localStorage
 |                   |                      |                      |
 |-- App loads ----> |                      |                      |
 |                   |-- Read token -------------------------------->
 |                   |<-- token (or null) ---------------------------
 |                   |-- GET /api/auth/me (Bearer token) ------->  |
 |                   |<-- 200 { user } OR 401                      |
 |                   |-- Populate AuthContext (or clear session)    |
  ]]></ac:plain-text-body>
</ac:structured-macro>
"""

PAGE_CONTENT["3.2 Browse and Search Products"] = """
<h2>User Journey: Browse the Catalogue</h2>
<ac:structured-macro ac:name="code">
  <ac:parameter ac:name="language">text</ac:parameter>
  <ac:plain-text-body><![CDATA[
User          React Frontend           Products Service
 |                   |                      |
 |-- Navigate /products ----------------->  |
 |                   |-- GET /api/products?sort=price_asc ------> |
 |                   |<-- 200 { total, products[] } -----------   |
 |                   |-- Render product grid                       |
 |<-- Product grid - |                                            |
 |                   |                      |
 |-- Apply category filter                  |
 |-- Apply type filter                      |
 |-- Apply price range                      |
 |-- Change sort order                      |
 |                   |-- GET /api/products?category=gold&sort=rating_desc ->
 |                   |<-- 200 { total, products[] }               |
 |                   |-- Re-render grid                            |
 |<-- Filtered results                      |
  ]]></ac:plain-text-body>
</ac:structured-macro>
<h2>User Journey: Search Products</h2>
<ac:structured-macro ac:name="code">
  <ac:parameter ac:name="language">text</ac:parameter>
  <ac:plain-text-body><![CDATA[
User          React Frontend           Products Service
 |                   |                      |
 |-- Type in search box                     |
 |                   |-- GET /api/products?search=diamond+necklace ->
 |                   |<-- 200 { total, products[] }               |
 |                   |-- Re-render grid                            |
 |<-- Search results |                      |

Notes:
 - Search triggers on every keystroke (debounced)
 - Searches across name, description, material, category, type
 - Empty search returns all products
  ]]></ac:plain-text-body>
</ac:structured-macro>
<h2>User Journey: View Product Detail</h2>
<ac:structured-macro ac:name="code">
  <ac:parameter ac:name="language">text</ac:parameter>
  <ac:plain-text-body><![CDATA[
User          React Frontend           Products Service
 |                   |                      |
 |-- Click product card                     |
 |                   |-- Navigate /products/:id                   |
 |                   |-- GET /api/products/{id} ----------------> |
 |                   |<-- 200 { product } OR 404                  |
 |                   |-- Render detail page                        |
 |<-- Product detail |                      |
  ]]></ac:plain-text-body>
</ac:structured-macro>
"""

PAGE_CONTENT["3.3 Add to Cart"] = """
<h2>User Journey: Add to Cart (Authenticated User)</h2>
<ac:structured-macro ac:name="code">
  <ac:parameter ac:name="language">text</ac:parameter>
  <ac:plain-text-body><![CDATA[
User          React Frontend           Cart Service           Auth Service
 |                   |                      |                      |
 |-- On /products/:id|                      |                      |
 |-- Select size ---> |                     |                      |
 |-- Select qty ----> |                     |                      |
 |-- Click Add to Cart                      |                      |
 |                   |-- User logged in? (check AuthContext)       |
 |                   |-- YES: POST /api/cart (Bearer token) ----> |
 |                   |                      |-- Validate JWT       |
 |                   |                      |-- Extract userId     |
 |                   |                      |-- Check if same productId+size exists
 |                   |                      |-- If yes: increment qty (cap at inventory)
 |                   |                      |-- If no: insert new row
 |                   |<-- 200 { items[] } --|                      |
 |                   |-- Update CartContext  |                      |
 |                   |-- Show "Added to cart!" for 2s             |
 |<-- Confirmation - |                      |                      |

Error paths:
 |                   |-- User NOT logged in: redirect to /login   |
 |                   |-- Size not selected: show "Please select a size."
 |                   |-- Out of stock (inventory=0): button disabled, shows "Out of Stock"
  ]]></ac:plain-text-body>
</ac:structured-macro>
<h2>User Journey: Manage Cart</h2>
<ac:structured-macro ac:name="code">
  <ac:parameter ac:name="language">text</ac:parameter>
  <ac:plain-text-body><![CDATA[
User          React Frontend           Cart Service
 |                   |                      |
 |-- Navigate /cart  |                      |
 |                   |-- GET /api/cart (Bearer token) ----------> |
 |                   |<-- 200 { items[] }   |                     |
 |                   |-- Render cart items  |                     |
 |<-- Cart page ---  |                      |                     |
 |                   |                      |
 |-- Change quantity |                      |
 |                   |-- PUT /api/cart/{itemId} { quantity } ---> |
 |                   |<-- 200 { items[] }   |                     |
 |                   |                      |
 |-- Remove item ---> |                     |
 |                   |-- DELETE /api/cart/{itemId} ------------> |
 |                   |<-- 200 { items[] }   |                     |
 |                   |                      |
 |-- Clear cart ----> |                     |
 |                   |-- DELETE /api/cart/clear ----------------> |
 |                   |<-- 200 { items: [] } |                     |
  ]]></ac:plain-text-body>
</ac:structured-macro>
"""

PAGE_CONTENT["3.4 Checkout and Place Order"] = """
<h2>User Journey: Checkout and Place Order</h2>
<ac:structured-macro ac:name="code">
  <ac:parameter ac:name="language">text</ac:parameter>
  <ac:plain-text-body><![CDATA[
User          React Frontend           Orders Service         Cart Service
 |                   |                      |                      |
 |-- Navigate /checkout                     |                      |
 |                   |-- ProtectedRoute: user logged in?          |
 |                   |-- NO: redirect to /login                   |
 |                   |-- YES: is cart empty?                      |
 |                   |-- YES: redirect to /cart                   |
 |                   |-- NO: render checkout form                 |
 |<-- Checkout form  |                      |                      |
 |                   |                      |                      |
 |-- Fill delivery address                  |                      |
 |-- Click "Place Order"                    |                      |
 |                   |-- Validate all required address fields      |
 |                   |-- Build order payload (cart snapshot + address + totals)
 |                   |-- POST /api/orders (Bearer token) ------->  |
 |                   |                      |-- Validate JWT       |
 |                   |                      |-- Extract userId     |
 |                   |                      |-- Persist order + items
 |                   |                      |-- Generate order number
 |                   |                      |-- Set estimatedDelivery = today + 5 days
 |                   |<-- 200 { order } --  |                      |
 |                   |-- DELETE /api/cart/clear (Bearer token) ----------->|
 |                   |<-- 200 { items: [] } |                      |
 |                   |-- Navigate to /orders (pass order in router state)
 |<-- Orders page with success banner       |                      |

Notes:
 - GST is calculated client-side at flat 3%
 - Payment model is Cash on Delivery -- no card processing
 - cardNumber field in request is accepted but ignored
  ]]></ac:plain-text-body>
</ac:structured-macro>
"""

PAGE_CONTENT["3.5 View Order History"] = """
<h2>User Journey: View Order History</h2>
<ac:structured-macro ac:name="code">
  <ac:parameter ac:name="language">text</ac:parameter>
  <ac:plain-text-body><![CDATA[
User          React Frontend           Orders Service
 |                   |                      |
 |-- Navigate /orders|                      |
 |                   |-- ProtectedRoute: user logged in?
 |                   |-- NO: redirect to /login
 |                   |-- YES: GET /api/orders (Bearer token) ---> |
 |                   |                      |-- Validate JWT       |
 |                   |                      |-- Extract userId     |
 |                   |                      |-- Fetch orders for user (newest first)
 |                   |<-- 200 { orders[] }  |
 |                   |-- Check router state for new order (success banner)
 |                   |-- Render order cards (collapsed)           |
 |<-- Order history  |                      |
 |                   |                      |
 |-- Click expand -> |                      |
 |                   |-- Render order items inline (no API call)  |
 |<-- Expanded order |                      |

Empty state:
 |                   |<-- 200 { orders: [] }|
 |                   |-- Show "No orders yet" + "Start Shopping" link
  ]]></ac:plain-text-body>
</ac:structured-macro>
"""

PAGE_CONTENT["4. Services"] = """
<p>This section documents each backend service and the frontend application in detail. Each sub-page covers purpose, database schema, all API endpoints with request/response contracts, and error handling.</p>
<table>
  <tbody>
    <tr><th>Service</th><th>Port</th><th>Auth</th><th>API Spec Repo</th></tr>
    <tr><td>Auth Service</td><td>3001</td><td>Public</td><td><a href="https://github.com/Mrithigha/gemstoneworld-auth-service">gemstoneworld-auth-service</a></td></tr>
    <tr><td>Products Service</td><td>3002</td><td>Public</td><td><a href="https://github.com/Mrithigha/gemstoneworld-products-service">gemstoneworld-products-service</a></td></tr>
    <tr><td>Cart Service</td><td>3003</td><td>JWT required</td><td><a href="https://github.com/Mrithigha/gemstoneworld-cart-service">gemstoneworld-cart-service</a></td></tr>
    <tr><td>Orders Service</td><td>3004</td><td>JWT required</td><td><a href="https://github.com/Mrithigha/gemstoneworld-orders-service">gemstoneworld-orders-service</a></td></tr>
    <tr><td>Frontend</td><td>5173</td><td>Context-dependent</td><td><a href="https://github.com/Mrithigha/gemstoneworld">gemstoneworld</a></td></tr>
  </tbody>
</table>
"""

PAGE_CONTENT["4.1 Auth Service"] = """
<h2>Overview</h2>
<table>
  <tbody>
    <tr><th>Property</th><th>Value</th></tr>
    <tr><td>Port</td><td>3001</td></tr>
    <tr><td>Base URL</td><td>http://localhost:3001/api/auth</td></tr>
    <tr><td>Database file</td><td>./data/auth-db</td></tr>
    <tr><td>H2 Console</td><td>http://localhost:3001/h2-console</td></tr>
    <tr><td>GitHub Repo</td><td><a href="https://github.com/Mrithigha/gemstoneworld-auth-service">gemstoneworld-auth-service</a></td></tr>
  </tbody>
</table>
<p>The Auth Service handles all user identity operations. It is the only service that creates JWT tokens. It stores user records in H2 with BCrypt-hashed passwords.</p>
<h2>Database Schema &mdash; users table</h2>
<table>
  <tbody>
    <tr><th>Column</th><th>Type</th><th>Constraints</th></tr>
    <tr><td>id</td><td>VARCHAR</td><td>Primary Key (UUID)</td></tr>
    <tr><td>name</td><td>VARCHAR</td><td>NOT NULL</td></tr>
    <tr><td>email</td><td>VARCHAR</td><td>NOT NULL, UNIQUE</td></tr>
    <tr><td>password</td><td>VARCHAR</td><td>NOT NULL (BCrypt hash)</td></tr>
    <tr><td>created_at</td><td>TIMESTAMP</td><td>NOT NULL</td></tr>
  </tbody>
</table>
<h2>API Endpoints</h2>
<table>
  <tbody>
    <tr><th>Method</th><th>Path</th><th>Auth</th><th>Description</th></tr>
    <tr><td>POST</td><td>/api/auth/register</td><td>None</td><td>Register new user, returns JWT</td></tr>
    <tr><td>POST</td><td>/api/auth/login</td><td>None</td><td>Login, returns JWT</td></tr>
    <tr><td>GET</td><td>/api/auth/me</td><td>Bearer JWT</td><td>Return current user profile</td></tr>
  </tbody>
</table>
<h2>POST /api/auth/register</h2>
<p><strong>Request body:</strong></p>
<ac:structured-macro ac:name="code">
  <ac:parameter ac:name="language">json</ac:parameter>
  <ac:plain-text-body><![CDATA[
{
  "name": "Priya Nair",
  "email": "priya@example.com",
  "password": "secret123"
}
  ]]></ac:plain-text-body>
</ac:structured-macro>
<p><strong>Response 200:</strong></p>
<ac:structured-macro ac:name="code">
  <ac:parameter ac:name="language">json</ac:parameter>
  <ac:plain-text-body><![CDATA[
{
  "token": "<jwt>",
  "user": { "id": "uuid", "name": "Priya Nair", "email": "priya@example.com" }
}
  ]]></ac:plain-text-body>
</ac:structured-macro>
<p><strong>Error responses:</strong> 400 if email already registered or password &lt; 6 chars.</p>
<h2>POST /api/auth/login</h2>
<p><strong>Request body:</strong></p>
<ac:structured-macro ac:name="code">
  <ac:parameter ac:name="language">json</ac:parameter>
  <ac:plain-text-body><![CDATA[
{ "email": "priya@example.com", "password": "secret123" }
  ]]></ac:plain-text-body>
</ac:structured-macro>
<p><strong>Response 200:</strong> Same structure as /register. <strong>Error:</strong> 401 if credentials invalid.</p>
<h2>GET /api/auth/me</h2>
<p>Requires <code>Authorization: Bearer &lt;token&gt;</code>. Returns <code>{ id, name, email }</code>. Returns 401 if token missing or expired.</p>
"""

PAGE_CONTENT["4.2 Products Service"] = """
<h2>Overview</h2>
<table>
  <tbody>
    <tr><th>Property</th><th>Value</th></tr>
    <tr><td>Port</td><td>3002</td></tr>
    <tr><td>Base URL</td><td>http://localhost:3002/api</td></tr>
    <tr><td>Database file</td><td>./data/products-db</td></tr>
    <tr><td>H2 Console</td><td>http://localhost:3002/h2-console</td></tr>
    <tr><td>GitHub Repo</td><td><a href="https://github.com/Mrithigha/gemstoneworld-products-service">gemstoneworld-products-service</a></td></tr>
  </tbody>
</table>
<p>The Products Service exposes the jewellery catalogue as a read-only public API. It supports filtering, searching, and sorting. Data is seeded at startup from an in-memory data initialiser &mdash; no auth is required on any endpoint.</p>
<h2>Database Schema</h2>
<p><strong>products table</strong></p>
<table>
  <tbody>
    <tr><th>Column</th><th>Type</th><th>Notes</th></tr>
    <tr><td>id</td><td>VARCHAR</td><td>Primary Key</td></tr>
    <tr><td>name</td><td>VARCHAR</td><td>&nbsp;</td></tr>
    <tr><td>description</td><td>VARCHAR</td><td>&nbsp;</td></tr>
    <tr><td>price</td><td>DECIMAL</td><td>INR</td></tr>
    <tr><td>category</td><td>VARCHAR</td><td>gold / silver / diamond / imitation</td></tr>
    <tr><td>type</td><td>VARCHAR</td><td>necklace / earring / ring / bracelet / pendant / chain</td></tr>
    <tr><td>material</td><td>VARCHAR</td><td>&nbsp;</td></tr>
    <tr><td>image_url</td><td>VARCHAR</td><td>&nbsp;</td></tr>
    <tr><td>rating</td><td>DECIMAL</td><td>0.0 &ndash; 5.0</td></tr>
    <tr><td>reviews</td><td>INT</td><td>&nbsp;</td></tr>
    <tr><td>in_stock</td><td>BOOLEAN</td><td>&nbsp;</td></tr>
  </tbody>
</table>
<p><strong>product_sizes table</strong></p>
<table>
  <tbody>
    <tr><th>Column</th><th>Type</th><th>Notes</th></tr>
    <tr><td>id</td><td>BIGINT</td><td>Primary Key (auto)</td></tr>
    <tr><td>product_id</td><td>VARCHAR</td><td>FK &rarr; products.id</td></tr>
    <tr><td>size</td><td>VARCHAR</td><td>e.g. S, M, L, XS</td></tr>
    <tr><td>inventory</td><td>INT</td><td>&nbsp;</td></tr>
  </tbody>
</table>
<h2>API Endpoints</h2>
<table>
  <tbody>
    <tr><th>Method</th><th>Path</th><th>Auth</th><th>Description</th></tr>
    <tr><td>GET</td><td>/api/products</td><td>None</td><td>List products with optional filters</td></tr>
    <tr><td>GET</td><td>/api/products/{id}</td><td>None</td><td>Get single product by ID</td></tr>
  </tbody>
</table>
<h2>GET /api/products &mdash; Query Parameters</h2>
<table>
  <tbody>
    <tr><th>Parameter</th><th>Type</th><th>Example</th><th>Notes</th></tr>
    <tr><td>category</td><td>string</td><td>gold</td><td>gold / silver / diamond / imitation</td></tr>
    <tr><td>type</td><td>string</td><td>ring</td><td>necklace / earring / ring / bracelet / pendant / chain</td></tr>
    <tr><td>search</td><td>string</td><td>diamond necklace</td><td>Searches name, description, material, category, type</td></tr>
    <tr><td>minPrice</td><td>number</td><td>500</td><td>INR</td></tr>
    <tr><td>maxPrice</td><td>number</td><td>50000</td><td>INR</td></tr>
    <tr><td>sort</td><td>string</td><td>price_asc</td><td>price_asc / price_desc / rating_desc / newest</td></tr>
  </tbody>
</table>
<p><strong>Response 200:</strong></p>
<ac:structured-macro ac:name="code">
  <ac:parameter ac:name="language">json</ac:parameter>
  <ac:plain-text-body><![CDATA[
{
  "total": 42,
  "products": [ { "id": "...", "name": "...", "price": 8800, "sizes": [...], ... } ]
}
  ]]></ac:plain-text-body>
</ac:structured-macro>
"""

PAGE_CONTENT["4.3 Cart Service"] = """
<h2>Overview</h2>
<table>
  <tbody>
    <tr><th>Property</th><th>Value</th></tr>
    <tr><td>Port</td><td>3003</td></tr>
    <tr><td>Base URL</td><td>http://localhost:3003/api</td></tr>
    <tr><td>Database file</td><td>./data/cart-db</td></tr>
    <tr><td>H2 Console</td><td>http://localhost:3003/h2-console</td></tr>
    <tr><td>GitHub Repo</td><td><a href="https://github.com/Mrithigha/gemstoneworld-cart-service">gemstoneworld-cart-service</a></td></tr>
  </tbody>
</table>
<p>The Cart Service manages per-user shopping carts. All endpoints require a valid JWT in the Authorization header. The service validates the JWT independently using the shared secret &mdash; it does not call the Auth Service.</p>
<h2>Database Schema &mdash; cart_items table</h2>
<table>
  <tbody>
    <tr><th>Column</th><th>Type</th><th>Notes</th></tr>
    <tr><td>id</td><td>BIGINT</td><td>Primary Key (auto)</td></tr>
    <tr><td>user_id</td><td>VARCHAR</td><td>From JWT subject claim</td></tr>
    <tr><td>product_id</td><td>VARCHAR</td><td>&nbsp;</td></tr>
    <tr><td>product_name</td><td>VARCHAR</td><td>Snapshot at add time</td></tr>
    <tr><td>price</td><td>DECIMAL</td><td>Snapshot at add time</td></tr>
    <tr><td>image_url</td><td>VARCHAR</td><td>&nbsp;</td></tr>
    <tr><td>size</td><td>VARCHAR</td><td>&nbsp;</td></tr>
    <tr><td>quantity</td><td>INT</td><td>&nbsp;</td></tr>
  </tbody>
</table>
<h2>API Endpoints</h2>
<table>
  <tbody>
    <tr><th>Method</th><th>Path</th><th>Auth</th><th>Description</th></tr>
    <tr><td>GET</td><td>/api/cart</td><td>Bearer JWT</td><td>Get current user&apos;s cart items</td></tr>
    <tr><td>POST</td><td>/api/cart</td><td>Bearer JWT</td><td>Add item to cart (or increment if exists)</td></tr>
    <tr><td>PUT</td><td>/api/cart/{itemId}</td><td>Bearer JWT</td><td>Update item quantity</td></tr>
    <tr><td>DELETE</td><td>/api/cart/{itemId}</td><td>Bearer JWT</td><td>Remove single item</td></tr>
    <tr><td>DELETE</td><td>/api/cart/clear</td><td>Bearer JWT</td><td>Remove all items for user</td></tr>
  </tbody>
</table>
<h2>POST /api/cart &mdash; Request Body</h2>
<ac:structured-macro ac:name="code">
  <ac:parameter ac:name="language">json</ac:parameter>
  <ac:plain-text-body><![CDATA[
{
  "productId": "gold-necklace-001",
  "productName": "Lakshmi Gold Necklace",
  "price": 28500,
  "imageUrl": "https://...",
  "size": "M",
  "quantity": 1
}
  ]]></ac:plain-text-body>
</ac:structured-macro>
<p>All endpoints return <code>200 { items: [...] }</code> &mdash; the full updated cart for the user. Returns 401 if JWT is missing or invalid.</p>
"""

PAGE_CONTENT["4.4 Orders Service"] = """
<h2>Overview</h2>
<table>
  <tbody>
    <tr><th>Property</th><th>Value</th></tr>
    <tr><td>Port</td><td>3004</td></tr>
    <tr><td>Base URL</td><td>http://localhost:3004/api</td></tr>
    <tr><td>Database file</td><td>./data/orders-db</td></tr>
    <tr><td>H2 Console</td><td>http://localhost:3004/h2-console</td></tr>
    <tr><td>GitHub Repo</td><td><a href="https://github.com/Mrithigha/gemstoneworld-orders-service">gemstoneworld-orders-service</a></td></tr>
  </tbody>
</table>
<p>The Orders Service persists placed orders and their line items. It validates JWTs locally using the shared secret. It does <strong>not</strong> call the Cart Service &mdash; the frontend provides the cart snapshot at checkout time.</p>
<h2>Database Schema</h2>
<p><strong>orders table</strong></p>
<table>
  <tbody>
    <tr><th>Column</th><th>Type</th><th>Notes</th></tr>
    <tr><td>id</td><td>BIGINT</td><td>Primary Key (auto)</td></tr>
    <tr><td>order_number</td><td>VARCHAR</td><td>e.g. GSW-20240115-001</td></tr>
    <tr><td>user_id</td><td>VARCHAR</td><td>From JWT subject claim</td></tr>
    <tr><td>status</td><td>VARCHAR</td><td>CONFIRMED / SHIPPED / DELIVERED</td></tr>
    <tr><td>subtotal</td><td>DECIMAL</td><td>INR</td></tr>
    <tr><td>gst</td><td>DECIMAL</td><td>3% of subtotal</td></tr>
    <tr><td>total</td><td>DECIMAL</td><td>subtotal + gst</td></tr>
    <tr><td>delivery_address</td><td>VARCHAR (JSON)</td><td>Serialised address object</td></tr>
    <tr><td>placed_at</td><td>TIMESTAMP</td><td>&nbsp;</td></tr>
    <tr><td>estimated_delivery</td><td>DATE</td><td>placed_at + 5 days</td></tr>
  </tbody>
</table>
<p><strong>order_items table</strong></p>
<table>
  <tbody>
    <tr><th>Column</th><th>Type</th><th>Notes</th></tr>
    <tr><td>id</td><td>BIGINT</td><td>Primary Key (auto)</td></tr>
    <tr><td>order_id</td><td>BIGINT</td><td>FK &rarr; orders.id</td></tr>
    <tr><td>product_id</td><td>VARCHAR</td><td>&nbsp;</td></tr>
    <tr><td>product_name</td><td>VARCHAR</td><td>&nbsp;</td></tr>
    <tr><td>price</td><td>DECIMAL</td><td>&nbsp;</td></tr>
    <tr><td>size</td><td>VARCHAR</td><td>&nbsp;</td></tr>
    <tr><td>quantity</td><td>INT</td><td>&nbsp;</td></tr>
    <tr><td>image_url</td><td>VARCHAR</td><td>&nbsp;</td></tr>
  </tbody>
</table>
<h2>API Endpoints</h2>
<table>
  <tbody>
    <tr><th>Method</th><th>Path</th><th>Auth</th><th>Description</th></tr>
    <tr><td>POST</td><td>/api/orders</td><td>Bearer JWT</td><td>Place a new order</td></tr>
    <tr><td>GET</td><td>/api/orders</td><td>Bearer JWT</td><td>Fetch all orders for current user (newest first)</td></tr>
  </tbody>
</table>
<h2>POST /api/orders &mdash; Request Body</h2>
<ac:structured-macro ac:name="code">
  <ac:parameter ac:name="language">json</ac:parameter>
  <ac:plain-text-body><![CDATA[
{
  "items": [
    { "productId": "gold-001", "productName": "Lakshmi Gold Necklace",
      "price": 28500, "size": "M", "quantity": 1, "imageUrl": "..." }
  ],
  "deliveryAddress": {
    "fullName": "Priya Nair", "phone": "9876543210",
    "addressLine1": "12 MG Road", "addressLine2": "",
    "city": "Chennai", "state": "Tamil Nadu",
    "pincode": "600001", "country": "India"
  },
  "subtotal": 28500,
  "gst": 855,
  "total": 29355,
  "cardNumber": ""
}
  ]]></ac:plain-text-body>
</ac:structured-macro>
<p><strong>Response 200:</strong> Full order object including <code>orderNumber</code> and <code>estimatedDelivery</code>.</p>
"""

PAGE_CONTENT["4.5 Frontend React UI"] = """
<h2>Overview</h2>
<table>
  <tbody>
    <tr><th>Property</th><th>Value</th></tr>
    <tr><td>Port</td><td>5173 (dev) / 4173 (preview)</td></tr>
    <tr><td>Framework</td><td>React 18 + Vite</td></tr>
    <tr><td>Router</td><td>React Router v6</td></tr>
    <tr><td>HTTP Client</td><td>Axios</td></tr>
    <tr><td>GitHub Repo</td><td><a href="https://github.com/Mrithigha/gemstoneworld">gemstoneworld</a></td></tr>
  </tbody>
</table>
<h2>Route Map</h2>
<table>
  <tbody>
    <tr><th>Path</th><th>Component</th><th>Auth Guard</th></tr>
    <tr><td>/</td><td>HomePage</td><td>None</td></tr>
    <tr><td>/products</td><td>ProductsPage</td><td>None</td></tr>
    <tr><td>/products/:id</td><td>ProductDetailPage</td><td>None</td></tr>
    <tr><td>/cart</td><td>CartPage</td><td>None (read) / JWT (modify)</td></tr>
    <tr><td>/checkout</td><td>CheckoutPage</td><td>ProtectedRoute</td></tr>
    <tr><td>/orders</td><td>OrdersPage</td><td>ProtectedRoute</td></tr>
    <tr><td>/login</td><td>LoginPage</td><td>None</td></tr>
    <tr><td>/register</td><td>RegisterPage</td><td>None</td></tr>
  </tbody>
</table>
<h2>Context Providers</h2>
<table>
  <tbody>
    <tr><th>Context</th><th>State</th><th>Persisted</th></tr>
    <tr><td>AuthContext</td><td>user, token, login(), logout()</td><td>localStorage (token + user JSON)</td></tr>
    <tr><td>CartContext</td><td>items[], addToCart(), removeFromCart(), updateQty(), clearCart()</td><td>No &mdash; fetched from Cart Service</td></tr>
  </tbody>
</table>
<h2>Service Base URLs (configured in src/services/api.js)</h2>
<table>
  <tbody>
    <tr><th>Constant</th><th>Value</th></tr>
    <tr><td>AUTH_API</td><td>http://localhost:3001/api/auth</td></tr>
    <tr><td>PRODUCTS_API</td><td>http://localhost:3002/api</td></tr>
    <tr><td>CART_API</td><td>http://localhost:3003/api</td></tr>
    <tr><td>ORDERS_API</td><td>http://localhost:3004/api</td></tr>
  </tbody>
</table>
<h2>Key Implementation Notes</h2>
<ul>
  <li>ProtectedRoute wraps /checkout and /orders &mdash; redirects unauthenticated users to /login.</li>
  <li>Add-to-cart on product detail redirects to /login if user is not authenticated.</li>
  <li>Cart count in navbar is derived from CartContext items.</li>
  <li>GST (3%) and totals are calculated client-side in the Checkout component.</li>
  <li>After order placement, cart is cleared via DELETE /api/cart/clear and navigation goes to /orders with a router state success flag.</li>
</ul>
"""

PAGE_CONTENT["5. Data Models Reference"] = """
<h2>Overview</h2>
<p>This page consolidates the key data shapes that flow between the frontend and backend services. All IDs are strings (UUID or auto-generated). All monetary values are in INR.</p>
<h2>User</h2>
<ac:structured-macro ac:name="code">
  <ac:parameter ac:name="language">json</ac:parameter>
  <ac:plain-text-body><![CDATA[
{
  "id": "uuid-string",
  "name": "Priya Nair",
  "email": "priya@example.com"
}
  ]]></ac:plain-text-body>
</ac:structured-macro>
<h2>Product</h2>
<ac:structured-macro ac:name="code">
  <ac:parameter ac:name="language">json</ac:parameter>
  <ac:plain-text-body><![CDATA[
{
  "id": "gold-necklace-001",
  "name": "Lakshmi Gold Necklace",
  "description": "22K gold necklace with temple design",
  "price": 28500,
  "category": "gold",
  "type": "necklace",
  "material": "22K Gold",
  "imageUrl": "https://...",
  "rating": 4.8,
  "reviews": 124,
  "inStock": true,
  "sizes": [
    { "size": "S", "inventory": 3 },
    { "size": "M", "inventory": 5 },
    { "size": "L", "inventory": 2 }
  ]
}
  ]]></ac:plain-text-body>
</ac:structured-macro>
<h2>Cart Item</h2>
<ac:structured-macro ac:name="code">
  <ac:parameter ac:name="language">json</ac:parameter>
  <ac:plain-text-body><![CDATA[
{
  "id": 42,
  "productId": "gold-necklace-001",
  "productName": "Lakshmi Gold Necklace",
  "price": 28500,
  "imageUrl": "https://...",
  "size": "M",
  "quantity": 1
}
  ]]></ac:plain-text-body>
</ac:structured-macro>
<h2>Order</h2>
<ac:structured-macro ac:name="code">
  <ac:parameter ac:name="language">json</ac:parameter>
  <ac:plain-text-body><![CDATA[
{
  "id": 7,
  "orderNumber": "GSW-20240115-007",
  "userId": "uuid-string",
  "status": "CONFIRMED",
  "items": [
    {
      "productId": "gold-necklace-001",
      "productName": "Lakshmi Gold Necklace",
      "price": 28500,
      "size": "M",
      "quantity": 1,
      "imageUrl": "https://..."
    }
  ],
  "deliveryAddress": {
    "fullName": "Priya Nair",
    "phone": "9876543210",
    "addressLine1": "12 MG Road",
    "addressLine2": "",
    "city": "Chennai",
    "state": "Tamil Nadu",
    "pincode": "600001",
    "country": "India"
  },
  "subtotal": 28500,
  "gst": 855,
  "total": 29355,
  "placedAt": "2024-01-15T10:30:00",
  "estimatedDelivery": "2024-01-20"
}
  ]]></ac:plain-text-body>
</ac:structured-macro>
<h2>JWT Payload</h2>
<ac:structured-macro ac:name="code">
  <ac:parameter ac:name="language">json</ac:parameter>
  <ac:plain-text-body><![CDATA[
{
  "sub": "uuid-string",   // userId
  "iat": 1705312200,
  "exp": 1705917000       // 7 days after iat
}
  ]]></ac:plain-text-body>
</ac:structured-macro>
"""

PAGE_CONTENT["6. How to Run Locally"] = """
<h2>Prerequisites</h2>
<table>
  <tbody>
    <tr><th>Tool</th><th>Version</th></tr>
    <tr><td>Node.js</td><td>18+</td></tr>
    <tr><td>npm</td><td>9+</td></tr>
    <tr><td>Java</td><td>17+</td></tr>
    <tr><td>Maven</td><td>3.8+</td></tr>
  </tbody>
</table>
<h2>Clone All Repositories</h2>
<ac:structured-macro ac:name="code">
  <ac:parameter ac:name="language">bash</ac:parameter>
  <ac:plain-text-body><![CDATA[
git clone https://github.com/Mrithigha/gemstoneworld
git clone https://github.com/Mrithigha/gemstoneworld-auth-service
git clone https://github.com/Mrithigha/gemstoneworld-products-service
git clone https://github.com/Mrithigha/gemstoneworld-cart-service
git clone https://github.com/Mrithigha/gemstoneworld-orders-service
  ]]></ac:plain-text-body>
</ac:structured-macro>
<h2>Start Backend Services</h2>
<p>Open a separate terminal for each service. Run them in any order &mdash; they are fully independent.</p>
<ac:structured-macro ac:name="code">
  <ac:parameter ac:name="language">bash</ac:parameter>
  <ac:plain-text-body><![CDATA[
# Terminal 1 — Auth Service (port 3001)
cd gemstoneworld-auth-service
mvn spring-boot:run

# Terminal 2 — Products Service (port 3002)
cd gemstoneworld-products-service
mvn spring-boot:run

# Terminal 3 — Cart Service (port 3003)
cd gemstoneworld-cart-service
mvn spring-boot:run

# Terminal 4 — Orders Service (port 3004)
cd gemstoneworld-orders-service
mvn spring-boot:run
  ]]></ac:plain-text-body>
</ac:structured-macro>
<h2>Start the Frontend</h2>
<ac:structured-macro ac:name="code">
  <ac:parameter ac:name="language">bash</ac:parameter>
  <ac:plain-text-body><![CDATA[
cd gemstoneworld
npm install
npm run dev
  ]]></ac:plain-text-body>
</ac:structured-macro>
<p>Open <a href="http://localhost:5173">http://localhost:5173</a> in your browser.</p>
<h2>H2 Consoles</h2>
<table>
  <tbody>
    <tr><th>Service</th><th>Console URL</th><th>JDBC URL</th></tr>
    <tr><td>Auth</td><td>http://localhost:3001/h2-console</td><td>jdbc:h2:file:./data/auth-db</td></tr>
    <tr><td>Products</td><td>http://localhost:3002/h2-console</td><td>jdbc:h2:file:./data/products-db</td></tr>
    <tr><td>Cart</td><td>http://localhost:3003/h2-console</td><td>jdbc:h2:file:./data/cart-db</td></tr>
    <tr><td>Orders</td><td>http://localhost:3004/h2-console</td><td>jdbc:h2:file:./data/orders-db</td></tr>
  </tbody>
</table>
<p>Username: <code>sa</code> &mdash; Password: (leave blank)</p>
<ac:structured-macro ac:name="info">
  <ac:parameter ac:name="title">First-time startup</ac:parameter>
  <ac:rich-text-body>
    <p>On first run, each service creates its H2 database file under <code>./data/</code> in the project directory. The Products Service seeds all 42 products automatically via a data initialiser bean. No manual SQL is needed.</p>
  </ac:rich-text-body>
</ac:structured-macro>
"""

PAGE_CONTENT["7. Testing Notes and Known Constraints"] = """
<h2>Testing Approach</h2>
<p>GemstoneWorld does not currently have automated test suites. Testing is performed manually by exercising the user journeys through the browser. The following notes capture known behaviours, edge cases, and constraints discovered during development.</p>
<h2>Known Constraints</h2>
<table>
  <tbody>
    <tr><th>Area</th><th>Constraint</th><th>Impact</th></tr>
    <tr><td>No API Gateway</td><td>Frontend hardcodes service base URLs in src/services/api.js</td><td>Changing port requires code change + rebuild</td></tr>
    <tr><td>No inventory decrement</td><td>Products Service does not reduce inventory on order placement</td><td>Inventory counts are display-only; overselling is possible</td></tr>
    <tr><td>No cart &rarr; orders sync</td><td>Orders Service does not call Cart Service</td><td>Frontend must send cart snapshot and then clear cart manually</td></tr>
    <tr><td>JWT in localStorage</td><td>Token stored in localStorage, not httpOnly cookie</td><td>Exposed to XSS attacks &mdash; acceptable for demo/dev</td></tr>
    <tr><td>Shared JWT secret</td><td>All services use the same hardcoded secret key</td><td>Rotating the key requires updating all four services simultaneously</td></tr>
    <tr><td>H2 file database</td><td>Each service writes to a local file</td><td>Not suitable for multi-instance deployment; data is per-machine</td></tr>
    <tr><td>No real payment</td><td>Checkout accepts any cardNumber string (or blank)</td><td>Payment is Cash on Delivery &mdash; no card validation</td></tr>
    <tr><td>GST client-side</td><td>3% GST calculated in the browser</td><td>Could be manipulated; no server-side validation of totals</td></tr>
    <tr><td>CORS origins hardcoded</td><td>Allowed origins: localhost:5173 and localhost:4173</td><td>Any other origin will be blocked</td></tr>
  </tbody>
</table>
<h2>Manual Test Checklist</h2>
<table>
  <tbody>
    <tr><th>#</th><th>Test Case</th><th>Expected Result</th></tr>
    <tr><td>1</td><td>Register with a new email</td><td>Redirected to home, user shown in navbar</td></tr>
    <tr><td>2</td><td>Register with duplicate email</td><td>Inline error: "Email already registered."</td></tr>
    <tr><td>3</td><td>Login with wrong password</td><td>Inline error: "Invalid email or password."</td></tr>
    <tr><td>4</td><td>Browse products without login</td><td>Full catalogue visible, no auth prompt</td></tr>
    <tr><td>5</td><td>Add to cart without login</td><td>Redirected to /login</td></tr>
    <tr><td>6</td><td>Add same product+size twice</td><td>Quantity increments on existing cart row</td></tr>
    <tr><td>7</td><td>Checkout with empty cart</td><td>Redirected to /cart</td></tr>
    <tr><td>8</td><td>Place order successfully</td><td>Redirected to /orders with success banner; cart cleared</td></tr>
    <tr><td>9</td><td>View orders page with no orders</td><td>"No orders yet" empty state shown</td></tr>
    <tr><td>10</td><td>Refresh page &mdash; session restored</td><td>User remains logged in; cart reloaded from Cart Service</td></tr>
    <tr><td>11</td><td>Filter by category + sort by price</td><td>Products re-fetched with correct filters applied</td></tr>
    <tr><td>12</td><td>Search returns zero results</td><td>Empty state shown in product grid</td></tr>
  </tbody>
</table>
<h2>Future Improvements</h2>
<ul>
  <li>Add automated integration tests (Spring Boot Test + MockMvc for services; Vitest + React Testing Library for frontend)</li>
  <li>Introduce an API gateway (e.g. Spring Cloud Gateway) to remove hardcoded URLs from the frontend</li>
  <li>Move JWT to httpOnly cookies to mitigate XSS risk</li>
  <li>Implement server-side inventory decrement on order placement</li>
  <li>Replace H2 with PostgreSQL for production readiness</li>
</ul>
"""

# ── Page creation sequence ────────────────────────────────────────────────────

print("=== Creating GemstoneWorld Confluence Pages ===\n")

# 1. Root page
print("1. Creating root page...")
root_id = create_page("GemstoneWorld — Engineering Hub", PAGE_CONTENT["GemstoneWorld — Engineering Hub"])

# 2. Top-level children
print("2. Creating '1. Application Overview'...")
p1_id = create_page("1. Application Overview", PAGE_CONTENT["1. Application Overview"], root_id)

print("3. Creating '2. High Level Design'...")
p2_id = create_page("2. High Level Design", PAGE_CONTENT["2. High Level Design"], root_id)

print("4. Creating '3. User Journey Sequence Diagrams'...")
p3_id = create_page("3. User Journey Sequence Diagrams", PAGE_CONTENT["3. User Journey Sequence Diagrams"], root_id)

# 3.x children
print("5. Creating '3.1 Register and Login'...")
create_page("3.1 Register and Login", PAGE_CONTENT["3.1 Register and Login"], p3_id)

print("6. Creating '3.2 Browse and Search Products'...")
create_page("3.2 Browse and Search Products", PAGE_CONTENT["3.2 Browse and Search Products"], p3_id)

print("7. Creating '3.3 Add to Cart'...")
create_page("3.3 Add to Cart", PAGE_CONTENT["3.3 Add to Cart"], p3_id)

print("8. Creating '3.4 Checkout and Place Order'...")
create_page("3.4 Checkout and Place Order", PAGE_CONTENT["3.4 Checkout and Place Order"], p3_id)

print("9. Creating '3.5 View Order History'...")
create_page("3.5 View Order History", PAGE_CONTENT["3.5 View Order History"], p3_id)

print("10. Creating '4. Services'...")
p4_id = create_page("4. Services", PAGE_CONTENT["4. Services"], root_id)

# 4.x children
print("11. Creating '4.1 Auth Service'...")
create_page("4.1 Auth Service", PAGE_CONTENT["4.1 Auth Service"], p4_id)

print("12. Creating '4.2 Products Service'...")
create_page("4.2 Products Service", PAGE_CONTENT["4.2 Products Service"], p4_id)

print("13. Creating '4.3 Cart Service'...")
create_page("4.3 Cart Service", PAGE_CONTENT["4.3 Cart Service"], p4_id)

print("14. Creating '4.4 Orders Service'...")
create_page("4.4 Orders Service", PAGE_CONTENT["4.4 Orders Service"], p4_id)

print("15. Creating '4.5 Frontend React UI'...")
create_page("4.5 Frontend React UI", PAGE_CONTENT["4.5 Frontend React UI"], p4_id)

print("16. Creating '5. Data Models Reference'...")
create_page("5. Data Models Reference", PAGE_CONTENT["5. Data Models Reference"], root_id)

print("17. Creating '6. How to Run Locally'...")
create_page("6. How to Run Locally", PAGE_CONTENT["6. How to Run Locally"], root_id)

print("18. Creating '7. Testing Notes and Known Constraints'...")
create_page("7. Testing Notes and Known Constraints", PAGE_CONTENT["7. Testing Notes and Known Constraints"], root_id)

print("\n=== All 18 pages created successfully! ===")
print(f"Space URL: https://mrithighasai.atlassian.net/wiki/spaces/{SPACE_KEY}/pages")
