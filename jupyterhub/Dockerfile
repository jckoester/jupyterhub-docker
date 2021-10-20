FROM jupyterhub/jupyterhub:1.4.2

COPY jupyterhub_config.py .

RUN pip install \
    dockerspawner \
    jupyterhub-idle-culler \
    oauthenticator
# Get ca-certifiactes for letsencrypt verification (https://discourse.jupyter.org/t/letsencrypt-certificate-verification-failed-after-09-30-2021/11058)
RUN apt-get update && apt-get install -yq --no-install-recommends \
    ca-certificates \
    libgnutls30 \
    && apt-get clean && rm -rf /var/lib/apt/lists/*