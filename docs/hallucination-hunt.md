# Hallucination Hunt — Lesson 2.7

The extractor is tested against these sample messages in
`code/lesson_2_7_extractor.py`. Before accepting extracted JSON, check it
against the original message and the trusted menu.

| Message | What to check |
|---|---|
| `Salam! 2 cupcakes aur 1 chocolate cake chahiye. Ali, house 12 Gulberg` | Items, quantities, customer, and address must be present in the source. |
| `hi do you deliver to Johar Town?` | This is a delivery question, not an order; the items list should be empty. |
| `1 pizza and 2 brownies` | Pizza is not on the menu; do not price or save it as a valid item. |
| `same as last time please` | There is no order detail in this message; do not infer a prior order. |
| `Bilal: 2 cakes, Model Town` | A generic cake is not necessarily a listed chocolate cake; do not silently change the item. |

The script validates item names against the menu, quantities against the
source text when they are explicit, and customer/address text against the
message. Each discrepancy is printed as `CHECK`; the final report summarizes
orders, combined total, and the number of checks. These checks reduce
hallucinations but do not replace human review.
