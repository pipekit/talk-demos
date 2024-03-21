FROM lucj/argocd-plugin-helmfile:latest
USER 0
RUN echo "  listenAddress: 0.0.0.0:8080" >> /home/argocd/cmp-server/config/plugin.yaml
USER 999
COPY --from=docker.io/joibel/argocd:latest /usr/local/bin/argocd-cmp-server /var/run/argocd/argocd-cmp-server
