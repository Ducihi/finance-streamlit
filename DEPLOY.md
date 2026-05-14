# Deploy the Finance Streamlit App

The recommended deployment path is Streamlit Community Cloud because this project is already a Streamlit app.

## Streamlit Community Cloud

1. Push this project to a GitHub repository.
2. Go to `https://share.streamlit.io`.
3. Create a new app.
4. Select the repository and branch.
5. Set the entrypoint file to `finance.py`.
6. Deploy the app and share the generated `streamlit.app` URL.

Notes:

- Keep `requirements.txt` in the repository root so Streamlit can install dependencies.
- Keep `.streamlit/config.toml` in the repository root for Streamlit configuration.
- The app must be public if you want anyone with the link to access it.
- Google Trends and Yahoo Finance calls depend on the deployed server's network access and upstream service availability.
- Google Trends is fetched through `pytrends`. If the deployed app shows a Google Trends warning, the most common cause is Google temporarily rate-limiting or blocking the cloud server IP. The app caches trend results for one hour to reduce repeat requests.
- If you change `requirements.txt`, reboot or redeploy the Streamlit app so dependency versions are rebuilt. This project pins `urllib3<2` for `pytrends` compatibility.

## Required Files

Make sure these files are all committed to GitHub in the same folder:

- `finance.py`
- `app.py`
- `data.py`
- `indicators.py`
- `trends.py`
- `requirements.txt`
- `.streamlit/config.toml`

If Streamlit shows `ModuleNotFoundError: No module named 'data'`, the deployment is usually missing `data.py`, or `finance.py` is not in the same folder as `data.py`.

## Render Web Service

Use Render if you want a standard public web service, custom domains, or paid always-on hosting.

1. Push this project to GitHub.
2. Create a new Render Web Service from the repository.
3. Render can use `render.yaml` automatically.
4. Confirm the start command:

```bash
streamlit run finance.py --server.port $PORT --server.address 0.0.0.0
```

Render web services must bind to `0.0.0.0` and the platform port so they can receive public traffic.

## Local Preview

```powershell
pip install -r requirements.txt
streamlit run finance.py
```

The old command also works:

```powershell
streamlit run app.py
```
