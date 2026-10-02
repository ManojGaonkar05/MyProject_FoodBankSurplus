# Folder 5 – GitHub Copilot generated code

**What to do (in VS Code with GitHub Copilot Chat):**
1. Open a new folder for the project code and start Copilot Chat.
2. Give it prompts based on the SRS, for example:
   - "Create an Express route POST /api/batches that lets a verified donor post a food batch with name, quantity, expiryAt and dietaryTags, and rejects an expiry time in the past."
   - "Write a function that checks a reservation: shelter verified, batch Available and not expired, then marks the batch Reserved so two shelters cannot reserve it."
   - "Write a Node.js scheduled job that sets Available batches to Expired when expiryAt has passed."
3. Read the code Copilot gives and fix anything wrong.

**What to save here:**
- [x] Screenshot of each prompt and Copilot reply (at least 3).
- [x] The generated code files, or the link to your code repository.
- [x] 2 or 3 lines on what you changed and why.

Repository link: https://github.com/ManojGaonkar05/foodbank-code 

   ## Summary
   - Prompt 1: Copilot created an Express app with POST /api/batches. It rejects past expiry times, missing dietary tags and invalid name/quantity. Only verified donors are allowed, and with no login system yet the default server returns 401 until authentication is added.
   - Prompt 2: reserveBatch in src/reservation.js checks the shelter is verified and the batch is Available and unexpired, then marks it Reserved, so a second shelter cannot reserve it.
   - Prompt 3: src/expiryJob.js marks Available batches as Expired every 60 seconds once expiryAt has passed.
   - All 13 tests pass with npm test.
   - I reviewed the generated code. Limitation: batches are stored in memory, so with MongoDB the reservation step must be an atomic database update to prevent double booking.

