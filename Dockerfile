FROM python:3.11

EXPOSE 53212/udp

RUN useradd -ms /bin/bash ewd
WORKDIR /home/ewd
USER ewd

COPY --chown=ewd:ewd . /home/ewd/

RUN pip install --no-cache-dir --user .

CMD python -m ewd_network_bridge
