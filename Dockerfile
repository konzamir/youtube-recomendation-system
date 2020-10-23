FROM python:3.6 AS base
COPY ./backend/requirements.txt /tmp/requirements.txt
RUN pip3 install --upgrade pip && \
    pip3 install --no-cache-dir -r /tmp/requirements.txt
RUN mkdir -p /usr/src/app
WORKDIR /usr/src/app
COPY ./backend /usr/src/app
# TODO:::add wait-for
EXPOSE 8000


FROM base AS backend-python
ENTRYPOINT python manage.py migrate && \
    python manage.py runserver 0.0.0.0:8000


FROM base AS backend-deploy
RUN pip install gunicorn==20.0.4


FROM backend-deploy AS backend-gunicorn
ENTRYPOINT python manage.py migrate && \
    gunicorn -b 0.0.0.0:8000 -w 4 --timeout 480 --max-requests 1000 --log-level debug main.wsgi


FROM node:12.2.0-alpine as build
WORKDIR /app
ENV PATH /app/node_modules/.bin:$PATH
COPY ./frontend/package.json /app/package.json
RUN npm install --silent
RUN npm install @vue/cli@3.7.0 -g
COPY ./frontend /app
RUN npm run build

# production environment
FROM nginx:1.16.0-alpine as prod-nginx
COPY --from=build /app/dist /usr/share/nginx/html
RUN rm /etc/nginx/conf.d/default.conf
COPY nginx/nginx.conf /etc/nginx/conf.d
EXPOSE 80
CMD ["nginx", "-g", "daemon off;"]

