
#!/bin/bash

PROFILE="piper-go-services"

echo "calling aws update configuration"
aws lambda update-function-configuration --function-name $1 --region $2 --profile $PROFILE --environment $3
