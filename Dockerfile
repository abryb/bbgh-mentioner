FROM ubuntu:18.04

ENV APT_KEY_DONT_WARN_ON_DANGEROUS_USAGE=1
ADD http://download.sgjp.pl/apt/sgjp.gpg.key /tmp/sgjp.gpg.key

RUN apt-get update \
    && apt-get install -y --no-install-recommends \
    python3 \
    python3-pip \
    software-properties-common \
    gpg-agent

RUN apt-key add /tmp/sgjp.gpg.key \
    && apt-add-repository http://download.sgjp.pl/apt/ubuntu \
    && apt-get update \
    && apt-get install -y --no-install-recommends libmorfeusz2-dev python3-morfeusz2 \
    && update-alternatives --install /usr/bin/python python /usr/bin/python3.6 1


# locale
RUN apt-get install -y --no-install-recommends locales && locale-gen en_US.UTF-8
ENV LANG en_US.UTF-8
ENV LANGUAGE en_US:en
ENV LC_ALL en_US.UTF-8

RUN rm -rf  /tmp/* && apt-get clean && rm -rf /var/lib/apt/lists/

WORKDIR /app

COPY requirements.txt .
RUN pip3 install -r requirements.txt

ENV PATH="/app/bin:${PATH}"

CMD ["mentioner", "--help"]
