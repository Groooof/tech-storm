FROM node:21 as build-stage-base
WORKDIR /opt/techstorm/frontend
COPY package.json package.json
RUN npm i --silent
COPY . .


FROM build-stage-base as build-local

FROM build-stage-base as build-dev
RUN npm run build-dev

FROM build-stage-base as build-prod
RUN npm run build-prod


FROM build-local as local-run
CMD ["npm", "run", "serve"]

FROM nginx:1.25.2 as dev-run
COPY --from=build-dev /opt/techstorm/frontend/dist /usr/share/nginx/html
COPY ./nginx/nginx.conf /etc/nginx/conf.d/default.conf
CMD ["nginx", "-g", "daemon off;"]

FROM nginx:1.25.2 as prod-run
COPY --from=build-prod /opt/techstorm/frontend/dist /usr/share/nginx/html
COPY ./nginx/nginx.conf /etc/nginx/conf.d/default.conf
CMD ["nginx", "-g", "daemon off;"]
