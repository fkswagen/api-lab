# API Lab Results

## Part 0

- Step 0.1, number of pizza names: **18** (current `GET /api/names` response).
- Step 0.3, status code of request to `/api/tools` without a token: **401 Unauthorized**.
- Step 0.4, name of vegetarian pizza: **A Lazy Siciliana** (current one-time vegetarian `POST /api/pizza` response).
- Step 0.12, three runs without a session: **Run 1: user creation 201, login 401, test failed. Run 2: user creation 201, login 401, test failed. Run 3: user creation 201, login 401, test failed.**
- The no-token `POST /api/ratings` case was not executed: live QuickPizza can create an unowned/orphaned rating without authorization, which violates the shared-service rule and cannot be safely tested.
- Step 0.16, blocks for how many of the three tools are excluded:
  - **0 tools excluded:** valid request; expected successful pizza response.
  - **1 tool excluded:** valid request; expected successful pizza response.
  - **2 tools excluded:** valid request; expected successful pizza response.
  - **3 tools excluded:** no pizza can satisfy request; expected **400** with a JSON error, but actual response was **500** with an empty body.

## Defect report

### Defect 1: Excluding every available tool causes an unhandled server error

- **Request:** `POST https://quickpizza.grafana.com/api/pizza` with a valid logged-in user's token and body:

  ```json
  {"excludedTools":["Knife","Pizza cutter","Scissors"]}
  ```

- **Expected result:** **400 Bad Request** with a JSON error message explaining that no pizza can satisfy the restrictions.
- **Actual result:** **500 Internal Server Error** with an empty response body.
- **Severity:** High. A valid, understandable client request produces an undocumented server failure and gives the client no parseable error.

## Part A: Ownership status codes

An authenticated second user attempted to access a rating created by its owner:

| Operation | Observed status | Result |
|---|---:|---|
| Cross-user GET | **404** | Refused; rating was not disclosed. |
| Cross-user PUT | **400** | Refused; rating was not changed. |
| Cross-user DELETE | **400** | Refused; rating was not deleted. |

All attempts returned 4xx responses, and an owner read confirmed that the rating remained unchanged.

## Part B

1. API tests can find failures that depend on the real network, such as DNS, TLS, connection, timeout,
   or routing failures. They can also find integration failures involving the deployed web server,
   authentication middleware, database, load balancer, or serialization. A unit test with stubs replaces
   those parts, so it cannot find those failures. Unit tests with stubs are still useful because they are
   fast, deterministic, and isolate one function, making business logic failures easier to diagnose.

2. Each test creates a user with a new made-up name so tests do not collide with one another or alter
   data belonging to another person. The public token is shared, so ratings created with it are shared
   too; another test could change or delete them while a test is running. In Project 2, I would create
   unique test records owned by my test account, use only credentials or tokens obtained by that account,
   and clean up records that the tests created. I would not modify shared shop or hotel data.

3. Every request uses one `requests.Session` because the session preserves cookies, including the
   `AWSALB` load-balancer cookie. QuickPizza stores a newly created user on one backend server, so
   preserving that cookie keeps the create and login requests on the same server. Without a session,
   the login can reach a different server that does not know the new user and can return 401. The three
   optional no-session outcomes were **401 login failures in all three runs** after user creation returned 201.

4. The block with **3 of 3 tools excluded** revealed the defect. No available tool can satisfy that
   request, so the API should return 400 and a JSON error that a client can parse and display. A 500
   with an empty body is worse because it looks like an internal crash, provides no usable explanation,
   and may cause a client to fail while parsing the response. The failing test remains as `xfail` rather
   than being deleted so the known defect stays visible. Strict `xfail` also makes the suite signal when
   the defect is fixed, prompting removal of the marker and conversion to a normal passing test.

5. Base choice needs 9 tests: one base test plus the non-base blocks for each characteristic:
   `1 + (3 - 1) + (4 - 1) + (2 - 1) + (3 - 1) = 9`. All-combinations coverage needs
   `3 × 4 × 2 × 3 = 72` tests. Base choice is smaller because it changes one characteristic at a time
   instead of testing every combination.

6. The other user's observed results were **GET 404**, **PUT 400**, and **DELETE 400**. I expected
   every attempt to be refused with a 4xx status; a consistent policy could use 403 Forbidden for an
   authenticated non-owner, or 404 Not Found to avoid revealing that the resource exists. The observed
   codes satisfy the lab's requirement that each attempt be refused with a 4xx response, and the owner
   check showed no unauthorized change or deletion. Therefore, the status-code difference alone is not
   a defect under this test requirement, although the API would be easier to document if it used one
   consistent ownership policy.

7. `GET https://quickpizza.grafana.com/api/ratings` with made-up token `0000000000000000` returned
   **200 OK** and included shared ratings. This is a security defect: the API accepted a token that was
   not obtained by logging in and exposed ratings to an unauthenticated stranger. On a real system,
   this could disclose users' data and violate access-control and privacy requirements. The made-up token
   was used only for this read; it was not used to create or change data.

8. An API test checks exact HTTP status codes, headers, JSON fields, and error bodies directly and
   repeatably. A web-page test can check things that an API test cannot see, such as rendered layout,
   visible controls, keyboard interaction, and accessibility of the user interface.
