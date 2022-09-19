FROM node:16

RUN npm install --global smee-client

CMD smee --url SMEE_ADDRESS \
  --target http://github-eventsource-svc:13000/push
