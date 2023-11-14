FROM nginx:1.25

COPY ./docker/prod/nginx/conf.d /etc/nginx/conf.d
COPY ./docker/prod/nginx/nginx.conf /etc/nginx/nginx.conf

CMD ["nginx", "-g", "daemon off;"]

EXPOSE 80