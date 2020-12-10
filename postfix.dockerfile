FROM tozd/postfix:alpine-38

ARG USERID
ARG GROUPID
#RUN adduser pl -D
RUN addgroup -g ${GROUPID} pl && \
    adduser -u ${USERID} -D -G pl pl