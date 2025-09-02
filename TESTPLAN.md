# Test Plan for COBOL Application

This test plan outlines the business logic and scenarios that need to be validated with the business stakeholders. Once validated, you can use this plan to create unit tests and integration tests for the Node.js application.

## Test Plan Table

| Test Case ID | Test Case Description                                   | Pre-conditions      | Test Steps                                                                                       | Expected Result                                             | Actual Result                                                                                  | Status (Pass/Fail) |
| ------------ | ------------------------------------------------------- | ------------------- | ------------------------------------------------------------------------------------------------ | ----------------------------------------------------------- | ---------------------------------------------------------------------------------------------- | ------------------ |
| TC-1.1       | View Current Balance                                    | Application started | 1. Start the application. <br> 2. Select option 1 to view the balance.                           | The application should display the current balance.         | Displays `Current balance: 1234.56` (balance preset in the test).                              | Pass               |
| TC-1.2       | View Balance with Various Presets                       | Application started | 1. Start the application. <br> 2. Preset different balances. <br> 3. Select option 1.            | Each preset balance is displayed correctly.                 | Displays `Current balance: X.XX` for 0.00, 12.34, 999.99, 1000.00.                             | Pass               |
| TC-2.1       | Credit Account with Valid Amount                        | Application started | 1. Start the application. <br> 2. Select option 2. <br> 3. Enter `50.00`.                        | Display the new balance after adding the credit amount.     | Displays `Amount credited. New balance: 150.00` and balance updated from `100.00` to `150.00`. | Pass               |
| TC-2.2       | Credit Account with Zero Amount                         | Application started | 1. Start the application. <br> 2. Select option 2. <br> 3. Enter `0.00`.                         | Balance unchanged.                                          | Displays `Amount must be positive.`; balance remains `100.00`.                                 | Pass               |
| TC-2.3       | Credit Multiple Valid Amounts                           | Application started | 1. Start the app. <br> 2. Select option 2 and enter various valid amounts.                       | New balance reflects each credit correctly.                 | Correct “Amount credited” messages; balances updated to expected values.                       | Pass               |
| TC-2.4       | Credit Invalid Non-numeric Input                        | Application started | 1. Start the app. <br> 2. Select option 2. <br> 3. Enter `""`, spaces, or `abc`.                 | Input rejected; balance unchanged.                          | Displays `Invalid amount.`; balance unchanged.                                                 | Pass               |
| TC-2.5       | Credit Negative Amount                                  | Application started | 1. Start the app. <br> 2. Select option 2. <br> 3. Enter negative values.                        | Input rejected; balance unchanged.                          | Displays `Amount must be positive.`; balance unchanged.                                        | Pass               |
| TC-3.1       | Debit Account with Valid Amount                         | Application started | 1. Start the application. <br> 2. Select option 3. <br> 3. Enter `50.00`.                        | Display the new balance after subtracting the debit amount. | Displays `Amount debited. New balance: 50.00` and balance updated from `100.00` to `50.00`.    | Pass               |
| TC-3.2       | Debit Account with Amount Greater Than Balance          | Application started | 1. Start the application. <br> 2. Select option 3. <br> 3. Enter `2000.00`.                      | Show "Insufficient funds" and keep balance.                 | Displays `Insufficient funds for this debit.`; balance remains `100.00`.                       | Pass               |
| TC-3.3       | Debit Account with Zero Amount                          | Application started | 1. Start the application. <br> 2. Select option 3. <br> 3. Enter `0.00`.                         | Balance unchanged.                                          | Displays `Amount must be positive.`; balance remains `100.00`.                                 | Pass               |
| TC-3.4       | Debit Multiple Valid Amounts                            | Application started | 1. Start the app. <br> 2. Select option 3 and enter various valid amounts.                       | New balance reflects each debit correctly.                  | Correct “Amount debited” messages; balances updated to expected values.                        | Pass               |
| TC-3.5       | Debit Insufficient Funds (various)                      | Application started | 1. Start the app. <br> 2. Select option 3. <br> 3. Enter amounts greater than balance.           | Show "Insufficient funds" and keep balance.                 | Displays `Insufficient funds for this debit.`; balance unchanged.                              | Pass               |
| TC-3.6       | Debit Negative Amount                                   | Application started | 1. Start the app. <br> 2. Select option 3. <br> 3. Enter negative values.                        | Input rejected; balance unchanged.                          | Displays `Amount must be positive.`; balance unchanged.                                        | Pass               |
| TC-3.7       | Debit Amount Equal to Balance                           | Application started | 1. Start the app. <br> 2. Select option 3. <br> 3. Enter amount equal to current balance.        | Balance becomes `0.00`.                                     | Displays `Amount debited. New balance: 0.00`; final balance `0.00`.                            | Pass               |
| TC-4.1       | Exit the Application                                    | Application started | 1. Start the application. <br> 2. Select option 4.                                               | Display exit message and terminate.                         | Displays `Exiting the program. Goodbye!` and exits the loop.                                   | Pass               |
| TC-4.2       | Execute Dispatch (TOTAL/CREDIT/DEBIT, case-insensitive) | Application started | 1. Call `execute` with `TOTAL`, `credit`, `DeBiT`.                                               | Correct function dispatched each time.                      | Dispatch prints sentinel outputs for TOTAL/CREDIT/DEBIT as expected.                           | Pass               |
| TC-4.3       | Execute Invalid Operation                               | Application started | 1. Call `execute` with `""`, `UNKNOWN`, `BALANCEZZ`.                                             | Print error message.                                        | Displays `Invalid operation.`                                                                  | Pass               |
| TC-4.4       | Menu CREDIT branch dispatch                             | Application started | 1. In menu: enter `2`, then `4`.                                                                 | `operations.execute("CREDIT")` called, then exit.           | Captured `DISPATCH:CREDIT` sentinel; exit message displayed.                                   | Pass               |
| TC-4.5       | Menu DEBIT branch dispatch                              | Application started | 1. In menu: enter `3`, then `4`.                                                                 | `operations.execute("DEBIT")` called, then exit.            | Captured `DISPATCH:DEBIT` sentinel; exit message displayed.                                    | Pass               |
| TC-5.1       | Sequence: Credit then Debit                             | Application started | Start `100.00` → credit `25.00` → debit `10.00`.                                                 | Final balance `115.00`.                                     | Balance ends at `115.00`.                                                                      | Pass               |
| TC-5.2       | Multiple Credits                                        | Application started | Start `0.00` → `+10.00` → `+20.00` → `+30.00`.                                                   | Final balance `60.00`.                                      | Balance ends at `60.00`.                                                                       | Pass               |
| TC-5.3       | Multiple Debits                                         | Application started | Start `200.00` → `-50.00` → `-50.00`.                                                            | Final balance `100.00`.                                     | Balance ends at `100.00`.                                                                      | Pass               |
| TC-6.1       | Credit then Insufficient Debit                          | Application started | Start `50.00` → `+25.00` → try `-100.00`.                                                        | Insufficient funds; balance unchanged after failure.        | Balance remains `75.00`.                                                                       | Pass               |
| TC-6.2       | Debit to Zero                                           | Application started | Start `75.00` → `-75.00`.                                                                        | Final balance `0.00`.                                       | Balance ends at `0.00`.                                                                        | Pass               |
| TC-7.1       | Execute Mixed Operations                                | Application started | `execute("CREDIT")` with `50.00`, then `execute("DEBIT")` with `25.00`, then `execute("TOTAL")`. | Final balance `125.00` and total displayed.                 | Balance `125.00`; total printed.                                                               | Pass               |
| TC-7.2       | Execute Invalid (trimmed)                               | Application started | Call `execute("   UNKNOWN   ")`.                                                                 | Print error message.                                        | Displays `Invalid operation.`                                                                  | Pass               |
| TC-8.1       | Large Credit Value                                      | Application started | Start `0.00` → credit `1,000,000,000.00`.                                                        | Balance reflects large credit.                              | Balance `1000000000.00`.                                                                       | Pass               |
| TC-8.2       | Large Debit Value                                       | Application started | Start `2,000,000,000.00` → debit `1,999,999,999.99`.                                             | Balance decreases to minimal remainder.                     | Balance `0.01`.                                                                                | Pass               |
| TC-9.1       | Credit with Whitespace Input                            | Application started | Start `100.00` → credit `"   25.00   "`.                                                         | Balance updated correctly.                                  | Balance `125.00`.                                                                              | Pass               |
| TC-9.2       | Debit with Whitespace Input                             | Application started | Start `200.00` → debit `"   25.00   "`.                                                          | Balance updated correctly.                                  | Balance `175.00`.                                                                              | Pass               |
| TC-9.3       | Credit Invalid then Valid                               | Application started | Start `50.00` → credit `"abc"` → credit `25.00`.                                                 | First rejected; second succeeds; final `75.00`.             | Balance `75.00`.                                                                               | Pass               |
| TC-9.4       | Debit Negative then Valid                               | Application started | Start `80.00` → debit `-10.00` → debit `30.00`.                                                  | First rejected; second succeeds; final `50.00`.             | Balance `50.00`.                                                                               | Pass               |
| TC-9.5       | Execute TOTAL with Spaces                               | Application started | Call `execute("   total   ")`.                                                                   | TOTAL executed after trim and case normalization.           | Displays `Current balance: 321.00` (with preset).                                              | Pass               |
| TC-9.6       | write_balance Quantizes to 2 Decimals                   | Application started | Call `write_balance(1.999)`.                                                                     | Stored value quantized to `2.00`.                           | Balance `2.00`.                                                                                | Pass               |
| TC-9.7       | Penny Credit then Penny Debit                           | Application started | Start `0.00` → `+0.01` → `-0.01`.                                                                | Final balance `0.00`.                                       | Balance `0.00`.                                                                                | Pass               |
| TC-9.8       | Alternating Operations End at Initial                   | Application started | Start `100.00` → `+10.00` → `-5.00` → `+0.50` → `-0.49` → `+4.99` → `-10.00`.                    | Final balance back to `100.00`.                             | Balance `100.00`.                                                                              | Pass               |
| TC-9.9       | Insufficient Debit After Prior Credit                   | Application started | Start `40.00` → `+10.00` → try `-100.00`.                                                        | Insufficient funds; balance stays `50.00`.                  | Displays insufficient funds; balance `50.00`.                                                  | Pass               |
| TC-9.10      | Large Credit then Large Debit to Penny                  | Application started | Start `0.00` → `+1,000,000.00` → `-999,999.99`.                                                  | Final balance `0.01`.                                       | Balance `0.01`.                                                                                | Pass               |

### Test Case TC-1.2: View Balance with Various Presets

**Description:** Verify that different preset balances are displayed correctly.

**Pre-conditions:** Application started.

**Test Steps:**

1. Start the application.
2. Preset the balance to values like 0.00, 12.34, 999.99, 1000.00.
3. Select option 1 to view the balance.

**Expected Result:** The application should display the correct balance for each preset.

**Actual Result:** Displays `Current balance: X.XX` for each preset.

**Status (Pass/Fail):** Pass

---

### Test Case TC-2.3: Credit Multiple Valid Amounts

**Description:** Verify that multiple valid credit amounts update the balance correctly.

**Pre-conditions:** Application started.

**Test Steps:**

1. Start the application.
2. Select option 2 and enter valid amounts like 0.01, 50.00, 90.00.
3. Repeat several times.

**Expected Result:** The balance increases correctly after each credit.

**Actual Result:** Displays correct "Amount credited" messages; balances updated as expected.

**Status (Pass/Fail):** Pass

---

### Test Case TC-2.4: Credit Invalid Non-numeric Input

**Description:** Verify that invalid non-numeric credit inputs are rejected.

**Pre-conditions:** Application started.

**Test Steps:**

1. Start the application.
2. Select option 2.
3. Enter values such as `""`, `"   "`, or `"abc"`.

**Expected Result:** Input is rejected and balance remains unchanged.

**Actual Result:** Displays `Invalid amount.`; balance unchanged.

**Status (Pass/Fail):** Pass

---

### Test Case TC-2.5: Credit Negative Amount

**Description:** Verify that negative credit amounts are rejected.

**Pre-conditions:** Application started.

**Test Steps:**

1. Start the application.
2. Select option 2.
3. Enter values such as `-1`, `-0.01`.

**Expected Result:** Input is rejected and balance remains unchanged.

**Actual Result:** Displays `Amount must be positive.`; balance unchanged.

**Status (Pass/Fail):** Pass

---

### Test Case TC-3.4: Debit Multiple Valid Amounts

**Description:** Verify that multiple valid debit amounts update the balance correctly.

**Pre-conditions:** Application started.

**Test Steps:**

1. Start the application.
2. Select option 3 and enter valid amounts like 0.01, 10.00, 5.00.
3. Repeat several times.

**Expected Result:** The balance decreases correctly after each debit.

**Actual Result:** Displays correct "Amount debited" messages; balances updated as expected.

**Status (Pass/Fail):** Pass

---

### Test Case TC-3.5: Debit Insufficient Funds

**Description:** Verify that debit amounts greater than the balance are rejected.

**Pre-conditions:** Application started.

**Test Steps:**

1. Start the application.
2. Select option 3.
3. Enter values such as 2000.00, 9999, or amounts slightly above balance.

**Expected Result:** Show "Insufficient funds" and balance remains unchanged.

**Actual Result:** Displays `Insufficient funds for this debit.`; balance unchanged.

**Status (Pass/Fail):** Pass

---

### Test Case TC-3.6: Debit Negative Amount

**Description:** Verify that negative debit amounts are rejected.

**Pre-conditions:** Application started.

**Test Steps:**

1. Start the application.
2. Select option 3.
3. Enter `-1` or `-0.01`.

**Expected Result:** Input is rejected and balance remains unchanged.

**Actual Result:** Displays `Amount must be positive.`; balance unchanged.

**Status (Pass/Fail):** Pass

---

### Test Case TC-3.7: Debit Amount Equal to Balance

**Description:** Verify that debiting the full balance sets it to zero.

**Pre-conditions:** Application started.

**Test Steps:**

1. Start the application.
2. Select option 3.
3. Enter the current balance (e.g., 100.00).

**Expected Result:** Balance becomes 0.00.

**Actual Result:** Displays `Amount debited. New balance: 0.00`; final balance is 0.00.

**Status (Pass/Fail):** Pass

---

### Test Case TC-4.2: Execute Dispatch (TOTAL/CREDIT/DEBIT)

**Description:** Verify that execute() dispatches operations correctly, case-insensitive.

**Pre-conditions:** Application started.

**Test Steps:**

1. Call execute with "TOTAL".
2. Call execute with "credit".
3. Call execute with " DeBiT ".

**Expected Result:** Each input dispatches to the correct function.

**Actual Result:** Sentinel outputs show TOTAL, CREDIT, and DEBIT executed.

**Status (Pass/Fail):** Pass

---

### Test Case TC-4.3: Execute Invalid Operation

**Description:** Verify that invalid operations are rejected.

**Pre-conditions:** Application started.

**Test Steps:**

1. Call execute with "", "UNKNOWN", "BALANCEZZ".

**Expected Result:** Error message displayed.

**Actual Result:** Displays `Invalid operation.`

**Status (Pass/Fail):** Pass

---

### Test Case TC-4.4: Menu CREDIT Branch Dispatch

**Description:** Verify that choosing option 2 in the menu calls CREDIT.

**Pre-conditions:** Application started.

**Test Steps:**

1. Select option 2.
2. Then select option 4 to exit.

**Expected Result:** CREDIT is dispatched, then exit message is shown.

**Actual Result:** Captured `DISPATCH:CREDIT` sentinel and exit message.

**Status (Pass/Fail):** Pass

---

### Test Case TC-4.5: Menu DEBIT Branch Dispatch

**Description:** Verify that choosing option 3 in the menu calls DEBIT.

**Pre-conditions:** Application started.

**Test Steps:**

1. Select option 3.
2. Then select option 4 to exit.

**Expected Result:** DEBIT is dispatched, then exit message is shown.

**Actual Result:** Captured `DISPATCH:DEBIT` sentinel and exit message.

**Status (Pass/Fail):** Pass

---

### Test Case TC-5.1: Sequence Credit then Debit

**Description:** Verify sequence of credit then debit updates balance correctly.

**Pre-conditions:** Application started.

**Test Steps:**

1. Start 100.00.
2. Credit 25.00.
3. Debit 10.00.

**Expected Result:** Final balance 115.00.

**Actual Result:** Balance ends at 115.00.

**Status (Pass/Fail):** Pass

---

### Test Case TC-5.2: Multiple Credits

**Description:** Verify multiple consecutive credits accumulate correctly.

**Pre-conditions:** Application started.

**Test Steps:**

1. Start 0.00.
2. Credit 10.00.
3. Credit 20.00.
4. Credit 30.00.

**Expected Result:** Final balance 60.00.

**Actual Result:** Balance ends at 60.00.

**Status (Pass/Fail):** Pass

---

### Test Case TC-5.3: Multiple Debits

**Description:** Verify multiple consecutive debits subtract correctly.

**Pre-conditions:** Application started.

**Test Steps:**

1. Start 200.00.
2. Debit 50.00.
3. Debit 50.00.

**Expected Result:** Final balance 100.00.

**Actual Result:** Balance ends at 100.00.

**Status (Pass/Fail):** Pass

---

### Test Case TC-6.1: Credit then Insufficient Debit

**Description:** Verify that after a credit, an excessive debit is still rejected.

**Pre-conditions:** Application started.

**Test Steps:**

1. Start 50.00.
2. Credit 25.00.
3. Attempt to debit 100.00.

**Expected Result:** Debit rejected; balance unchanged at 75.00.

**Actual Result:** Balance remains 75.00.

**Status (Pass/Fail):** Pass

---

### Test Case TC-6.2: Debit to Zero Balance

**Description:** Verify debiting the entire balance reduces it to zero.

**Pre-conditions:** Application started.

**Test Steps:**

1. Start 75.00.
2. Debit 75.00.

**Expected Result:** Balance becomes 0.00.

**Actual Result:** Balance ends at 0.00.

**Status (Pass/Fail):** Pass

---

### Test Case TC-7.1: Execute Mixed Operations

**Description:** Verify execute() correctly calls TOTAL, CREDIT, and DEBIT in sequence.

**Pre-conditions:** Application started.

**Test Steps:**

1. Credit 50.00 via execute.
2. Debit 25.00 via execute.
3. Call TOTAL via execute.

**Expected Result:** Final balance 125.00; TOTAL displayed.

**Actual Result:** Balance 125.00; total printed.

**Status (Pass/Fail):** Pass

---

### Test Case TC-7.2: Execute Invalid (trimmed)

**Description:** Verify execute() rejects invalid operation with extra spaces.

**Pre-conditions:** Application started.

**Test Steps:**

1. Call execute(" UNKNOWN ").

**Expected Result:** Error message displayed.

**Actual Result:** Displays `Invalid operation.`

**Status (Pass/Fail):** Pass

---

### Test Case TC-8.1: Large Credit Value

**Description:** Verify system handles very large credit values.

**Pre-conditions:** Application started.

**Test Steps:**

1. Start 0.00.
2. Credit 1,000,000,000.00.

**Expected Result:** Balance reflects large credit.

**Actual Result:** Balance 1000000000.00.

**Status (Pass/Fail):** Pass

---

### Test Case TC-8.2: Large Debit Value

**Description:** Verify system handles very large debit values when funds are available.

**Pre-conditions:** Application started.

**Test Steps:**

1. Start 2,000,000,000.00.
2. Debit 1,999,999,999.99.

**Expected Result:** Balance decreases to minimal remainder.

**Actual Result:** Balance 0.01.

**Status (Pass/Fail):** Pass

---

### Test Case TC-9.1: Credit with Whitespace Input

**Description:** Verify that credit with whitespace around the input is accepted.

**Pre-conditions:** Application started.

**Test Steps:**

1. Start 100.00.
2. Credit " 25.00 ".

**Expected Result:** Balance increases correctly.

**Actual Result:** Balance 125.00.

**Status (Pass/Fail):** Pass

---

### Test Case TC-9.2: Debit with Whitespace Input

**Description:** Verify that debit with whitespace around the input is accepted.

**Pre-conditions:** Application started.

**Test Steps:**

1. Start 200.00.
2. Debit " 25.00 ".

**Expected Result:** Balance decreases correctly.

**Actual Result:** Balance 175.00.

**Status (Pass/Fail):** Pass

---

### Test Case TC-9.3: Credit Invalid then Valid

**Description:** Verify invalid credit input is rejected but a subsequent valid credit succeeds.

**Pre-conditions:** Application started.

**Test Steps:**

1. Start 50.00.
2. Credit "abc" (invalid).
3. Credit 25.00 (valid).

**Expected Result:** First rejected; second succeeds; final balance 75.00.

**Actual Result:** Balance 75.00.

**Status (Pass/Fail):** Pass

---

### Test Case TC-9.4: Debit Negative then Valid

**Description:** Verify negative debit is rejected but a valid debit succeeds after.

**Pre-conditions:** Application started.

**Test Steps:**

1. Start 80.00.
2. Debit -10.00 (invalid).
3. Debit 30.00 (valid).

**Expected Result:** First rejected; second succeeds; final balance 50.00.

**Actual Result:** Balance 50.00.

**Status (Pass/Fail):** Pass

---

### Test Case TC-9.5: Execute TOTAL with Spaces

**Description:** Verify execute() trims spaces and normalizes case.

**Pre-conditions:** Application started.

**Test Steps:**

1. Call execute(" total ").

**Expected Result:** TOTAL is executed.

**Actual Result:** Displays `Current balance: 321.00`.

**Status (Pass/Fail):** Pass

---

### Test Case TC-9.6: write_balance Quantizes to 2 Decimals

**Description:** Verify that write_balance always stores 2 decimal places.

**Pre-conditions:** Application started.

**Test Steps:**

1. Call write_balance(1.999).

**Expected Result:** Balance stored as 2.00.

**Actual Result:** Balance 2.00.

**Status (Pass/Fail):** Pass

---

### Test Case TC-9.7: Penny Credit then Penny Debit

**Description:** Verify crediting and debiting a penny results in 0.00 balance.

**Pre-conditions:** Application started.

**Test Steps:**

1. Start 0.00.
2. Credit 0.01.
3. Debit 0.01.

**Expected Result:** Balance 0.00.

**Actual Result:** Balance 0.00.

**Status (Pass/Fail):** Pass

---

### Test Case TC-9.8: Alternating Operations End at Initial

**Description:** Verify a sequence of alternating operations returns to initial balance.

**Pre-conditions:** Application started.

**Test Steps:**

1. Start 100.00.
2. Credit 10.00.
3. Debit 5.00.
4. Credit 0.50.
5. Debit 0.49.
6. Credit 4.99.
7. Debit 10.00.

**Expected Result:** Final balance back to 100.00.

**Actual Result:** Balance 100.00.

**Status (Pass/Fail):** Pass

---

### Test Case TC-9.9: Insufficient Debit After Prior Credit

**Description:** Verify insufficient debit after a valid credit is rejected.

**Pre-conditions:** Application started.

**Test Steps:**

1. Start 40.00.
2. Credit 10.00.
3. Attempt to debit 100.00.

**Expected Result:** Debit rejected; balance remains 50.00.

**Actual Result:** Balance 50.00.

**Status (Pass/Fail):** Pass

---

### Test Case TC-9.10: Large Credit then Large Debit to Penny

**Description:** Verify large credit followed by large debit leaves minimal remainder.

**Pre-conditions:** Application started.

**Test Steps:**

1. Start 0.00.
2. Credit 1,000,000.00.
3. Debit 999,999.99.

**Expected Result:** Final balance 0.01.

**Actual Result:** Balance 0.01.

**Status (Pass/Fail):** Pass

---

## Summary

This test plan covers the main functionalities of the Python application, including viewing the balance, crediting the account, debiting the account, and exiting the application. Validate this test plan with the business stakeholders to ensure it meets the business requirements. Once validated, you can use this plan to create corresponding unit tests and integration tests for the Python application.
