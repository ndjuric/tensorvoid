.PHONY: setup

setup:
	@if [ ! -d "venv" ]; then \
		echo "⚡ Creating Python virtual environment..."; \
		python3 -m venv venv; \
	fi
	@echo "⚡ Installing tensorvoid package and dependencies..."
	@./venv/bin/pip install -e .
	@echo ""
	@echo "=========================================================="
	@echo "⚡ Environment ready! Run 'source venv/bin/activate' to enter it,"
	@echo "then type 'tensorvoid' to launch the Setup Station."
	@echo "=========================================================="
