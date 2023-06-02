# Base image
FROM --platform=linux/amd64 nginx

COPY letterbox.conf /etc/nginx/conf.d

EXPOSE 80

CMD ["nginx", "-g", "daemon off;"]