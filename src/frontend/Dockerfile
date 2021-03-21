FROM alpine:3.12
RUN apk add --update --no-cache build-base bash curl nodejs npm
RUN npm i -g @vue/cli \
    @vue/cli-service \
    @vue/cli-plugin-babel \
    @vue/cli-plugin-eslint \
    @vue/cli-plugin-pwa \
    @vue/cli-plugin-typescript \
    @vue/cli-plugin-unit-jest