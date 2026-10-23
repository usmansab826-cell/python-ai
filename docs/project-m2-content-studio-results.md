# Module 2 Checkpoint 1: Test Results

Run offline checks with:

```powershell
uv run python -m unittest tests.test_coursework_projects -v
```

The automated tests check that the content brief carries the supplied audience
and verified facts, and that the review helper flags numbers absent from the
facts supplied by the business. The app requests structured output and reports
drafts that exceed the word limit or include unsupported numbers. These checks
do not prove every verbal claim is true; a person must still review the copy.

The live Ollama run demonstrated why this review is needed: an earlier draft
added unsupported claims such as “freshly made” and “special offers” and
incorrectly said all products were under 1,500 PKR. The app therefore treats
model text as a draft, flags some mechanical issues, and explicitly tells the
owner to review all claims before publishing.
