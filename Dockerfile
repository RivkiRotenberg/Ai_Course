FROM mcr.microsoft.com/powershell:latest

# Create a non-root user for safer execution
RUN useradd -m runner
USER runner
WORKDIR /home/runner

# copy the small entrypoint that runs the requested command inside PowerShell
COPY run_in_container.sh /home/runner/run_in_container.sh
RUN chmod +x /home/runner/run_in_container.sh

ENTRYPOINT ["/home/runner/run_in_container.sh"]
