FROM python:3.8 AS backend-base
COPY ./backend/requirements.txt /tmp/requirements.txt
RUN pip3 install --upgrade pip && \
    pip3 install --no-cache-dir -r /tmp/requirements.txt
RUN mkdir -p /usr/src/app
WORKDIR /usr/src/app
COPY ./backend /usr/src/app
ENV PYTHONPATH=.
# TODO:::add wait-for


FROM backend-base AS backend-gunicorn
EXPOSE 8000
RUN pip install gunicorn==20.0.4
ENTRYPOINT python manage.py migrate && \
    gunicorn -b 0.0.0.0:8000 -w 4 --timeout 480 --max-requests 1000 --log-level debug main.wsgi


FROM node:12.2.0-alpine as frontend-build
WORKDIR /app
ENV PATH /app/node_modules/.bin:$PATH
COPY ./frontend/package.json /app/package.json
RUN npm install --silent
RUN npm install @vue/cli@3.7.0 -g
COPY ./frontend /app
RUN npm run build


FROM nginx:1.16.0-alpine as prod-nginx
COPY --from=frontend-build /app/dist /usr/share/nginx/html
COPY --from=backend-gunicorn /usr/src/app/static /usr/share/nginx/static
RUN rm /etc/nginx/conf.d/default.conf
COPY nginx/nginx.conf /etc/nginx/conf.d
EXPOSE 80
CMD ["nginx", "-g", "daemon off;"]
