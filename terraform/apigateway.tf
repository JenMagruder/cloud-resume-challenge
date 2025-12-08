# HTTP API Gateway for Visitor Counter
# Connects the website to the Lambda function

resource "aws_apigatewayv2_api" "visitor_counter" {
  name          = "visitor-counter-api"
  protocol_type = "HTTP"
  
  cors_configuration {
    allow_origins = ["*"]
    allow_methods = ["POST", "OPTIONS"]
    allow_headers = ["content-type"]
  }

  tags = {
    Name        = "Visitor Counter API"
    Environment = "Production"
    ManagedBy   = "Terraform"
  }
}

# Lambda Integration

resource "aws_apigatewayv2_integration" "lambda" {
  api_id             = aws_apigatewayv2_api.visitor_counter.id
  integration_type   = "AWS_PROXY"
  integration_uri    = aws_lambda_function.visitor_counter.invoke_arn
  payload_format_version = "2.0"
}

# Route

resource "aws_apigatewayv2_route" "post" {
  api_id    = aws_apigatewayv2_api.visitor_counter.id
  route_key = "POST /count"
  target    = "integrations/${aws_apigatewayv2_integration.lambda.id}"
}

# Stage

resource "aws_apigatewayv2_stage" "default" {
  api_id      = aws_apigatewayv2_api.visitor_counter.id
  name        = "$default"
  auto_deploy = true

  tags = {
    Name        = "Default Stage"
    Environment = "Production"
    ManagedBy   = "Terraform"
  }
}

# Lambda Permission - Allow API Gateway to Invoke Lambda

resource "aws_lambda_permission" "api_gateway" {
  statement_id  = "AllowAPIGatewayInvoke"
  action        = "lambda:InvokeFunction"
  function_name = aws_lambda_function.visitor_counter.function_name
  principal     = "apigateway.amazonaws.com"
  source_arn    = "${aws_apigatewayv2_api.visitor_counter.execution_arn}/*/*"
}