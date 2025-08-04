# Snowflake Connector CVE-2025-24793 PoC

This repository contains Proof of Concept (PoC) code for testing CVE-2025-24793 vulnerability in Snowflake Connector for Python. The project includes both patched and unpatched versions to demonstrate the vulnerability and its fix.

## Prerequisites

- Docker installed on your system
- Snowflake account with appropriate permissions
- Basic understanding of Docker and Snowflake

## Repository Structure

```
├── Dockerfile                          # Docker configuration
├── requirements.txt                    # Python dependencies
├── config.toml                        # Snowflake connection configuration (you need to create this)
├── cve_2025_24793_poc.py              # Main PoC script (auto-detects patched/unpatched)
├── snowflake_app.py                   # Main application
└── snowflake_connector_python-2.9.0-py3-none-any.whl  # Snowflake connector wheel
```

## Setup Instructions

### 1. Prepare Build Files

Simply replace `snowflake_connector_python-2.9.0-py3-none-any.whl` with your build:
- **For Unpatched Build**: Use your unpatched/vulnerable wheel
- **For Patched Build**: Use your patched/fixed wheel

The PoC script will automatically detect which version you're using.

### 2. Create Snowflake Account and Configuration

1. **Create a Snowflake Account:**
   - Go to [Snowflake](https://www.snowflake.com/) and create a free trial account
   - Note down your account identifier (e.g., `abc123.us-east-1`)

2. **Create `config.toml` file:**
   
   Create a `config.toml` file in the root directory with your Snowflake credentials:

   ```toml
   [connections.my_example_connection]
   account = "your_account_identifier"    # e.g., "abc123.us-east-1"
   user = "your_username"                 # Your Snowflake username
   password = "your_password"             # Your Snowflake password
   role = "your_role"                     # e.g., "ACCOUNTADMIN" or "SYSADMIN"
   warehouse = "your_warehouse"           # e.g., "COMPUTE_WH"
   database = "your_database"             # e.g., "TESTDB"
   schema = "your_schema"                 # e.g., "PUBLIC"
   ```

   **Example configuration:**
   ```toml
   [connections.my_example_connection]
   account = "abc123.us-east-1"
   user = "testuser"
   password = "MySecurePassword123!"
   role = "ACCOUNTADMIN"
   warehouse = "COMPUTE_WH"
   database = "TESTDB"
   schema = "PUBLIC"
   ```

### 3. Build and Run

**Build Docker image:**
```bash
docker build -t <container_name> .
```

**Run Docker container:**
```bash
docker run --rm <container_name>
```

## Example Usage

**Testing with any build:**
```bash
# 1. Replace wheel with your patched or unpatched version
# 2. Build and run - the script will auto-detect the version
docker build -t snowflake-test .
docker run --rm snowflake-test
```

The PoC will automatically:
- Detect if you're using a patched or unpatched version
- Run appropriate tests based on the detected version
- Show clear output indicating the vulnerability status

## Understanding the Vulnerability

### CVE-2025-24793
This vulnerability affects the Snowflake Connector for Python and involves SQL injection through the `write_pandas` function.

The PoC script automatically detects and demonstrates:
- **Unpatched Version**: Shows vulnerable behavior with SQL injection attacks
- **Patched Version**: Shows that the vulnerability has been fixed

### Auto-Detection Feature
The script inspects the `write_pandas` function to determine if the vulnerable `stage_location` parameter is present, providing clear feedback on the security status.

## Important Notes

⚠️ **Security Warning**: This is a proof-of-concept for educational and testing purposes only. Do not use in production environments.

⚠️ **Configuration Security**: Never commit your `config.toml` file with real credentials to version control. Add it to `.gitignore`.

⚠️ **Snowflake Costs**: Be aware that running these tests may consume Snowflake compute credits.

## Troubleshooting

### Common Issues

1. **Authentication Errors**: Verify your Snowflake credentials in `config.toml`
2. **Network Issues**: Ensure your Docker container can reach Snowflake endpoints
3. **Permission Errors**: Make sure your Snowflake user has appropriate permissions

### Docker Issues

- If build fails, ensure all required files are present
- Check Docker daemon is running
- Verify Python dependencies in `requirements.txt`

