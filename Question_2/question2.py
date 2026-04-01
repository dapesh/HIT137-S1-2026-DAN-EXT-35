from __future__ import annotations

from pathlib import Path
import sys


def format_number(value: float) -> str:
	if float(value).is_integer():
		return str(int(value))
	text = f"{value:.10f}".rstrip("0").rstrip(".")
	return text if text else "0"


def format_result(value: float) -> str:
	if float(value).is_integer():
		return str(int(value))
	return f"{value:.4f}"


def tokenize(expression: str) -> list[dict]:
	tokens: list[dict] = []
	i = 0
	n = len(expression)

	while i < n:
		ch = expression[i]

		if ch.isspace():
			i += 1
			continue

		if ch in "+-*/":
			tokens.append({"type": "OP", "value": ch})
			i += 1
			continue

		if ch == "(":
			tokens.append({"type": "LPAREN", "value": "("})
			i += 1
			continue

		if ch == ")":
			tokens.append({"type": "RPAREN", "value": ")"})
			i += 1
			continue

		if ch.isdigit() or ch == ".":
			start = i
			has_digit = ch.isdigit()
			has_dot = ch == "."
			i += 1

			while i < n:
				nxt = expression[i]
				if nxt.isdigit():
					has_digit = True
					i += 1
				elif nxt == "." and not has_dot:
					has_dot = True
					i += 1
				else:
					break

			lexeme = expression[start:i]
			if not has_digit:
				raise ValueError("Invalid number literal")

			number_value = float(lexeme)
			tokens.append({"type": "NUM", "value": lexeme, "number": number_value})
			continue

		raise ValueError(f"Invalid character: {ch}")

	tokens.append({"type": "END", "value": ""})
	return tokens


def tokens_to_output(tokens: list[dict]) -> str:
	parts: list[str] = []
	for token in tokens:
		token_type = token["type"]
		if token_type == "NUM":
			parts.append(f"[NUM:{token['value']}]")
		elif token_type == "END":
			parts.append("[END]")
		elif token_type == "OP":
			parts.append(f"[OP:{token['value']}]")
		elif token_type == "LPAREN":
			parts.append("[LPAREN:(]")
		elif token_type == "RPAREN":
			parts.append("[RPAREN:)]")
	return " ".join(parts)


def evaluate_tokens(tokens: list[dict]) -> tuple[str, float]:
	pos = 0

	def current() -> dict:
		return tokens[pos]

	def consume(expected_type: str, expected_value: str | None = None) -> dict:
		nonlocal pos
		tok = current()
		if tok["type"] != expected_type:
			raise ValueError("Unexpected token")
		if expected_value is not None and tok["value"] != expected_value:
			raise ValueError("Unexpected token value")
		pos += 1
		return tok

	def starts_factor(tok: dict) -> bool:
		if tok["type"] in {"NUM", "LPAREN"}:
			return True
		return False

	def parse_expression() -> tuple[str, float]:
		left_tree, left_value = parse_term()
		while current()["type"] == "OP" and current()["value"] in {"+", "-"}:
			op = consume("OP")["value"]
			right_tree, right_value = parse_term()
			if op == "+":
				left_value = left_value + right_value
			else:
				left_value = left_value - right_value
			left_tree = f"({op} {left_tree} {right_tree})"
		return left_tree, left_value

	def parse_term() -> tuple[str, float]:
		left_tree, left_value = parse_factor()

		while True:
			tok = current()

			if tok["type"] == "OP" and tok["value"] in {"*", "/"}:
				op = consume("OP")["value"]
				right_tree, right_value = parse_factor()
				if op == "*":
					left_value = left_value * right_value
				else:
					division_tree = f"(/ {left_tree} {right_tree})"
					if right_value == 0:
						raise ValueError(f"DIV_ZERO::{division_tree}")
					left_value = left_value / right_value
				left_tree = f"({op} {left_tree} {right_tree})"
				continue

			if starts_factor(tok):
				right_tree, right_value = parse_factor()
				left_value = left_value * right_value
				left_tree = f"(* {left_tree} {right_tree})"
				continue

			break

		return left_tree, left_value

	def parse_factor() -> tuple[str, float]:
		tok = current()

		if tok["type"] == "OP" and tok["value"] == "-":
			consume("OP", "-")
			operand_tree, operand_value = parse_factor()
			return f"(neg {operand_tree})", -operand_value

		if tok["type"] == "OP" and tok["value"] == "+":
			raise ValueError("Unary plus is not supported")

		return parse_primary()

	def parse_primary() -> tuple[str, float]:
		tok = current()

		if tok["type"] == "NUM":
			consume("NUM")
			number_value = tok["number"]
			return format_number(number_value), number_value

		if tok["type"] == "LPAREN":
			consume("LPAREN")
			inner_tree, inner_value = parse_expression()
			consume("RPAREN")
			return inner_tree, inner_value

		raise ValueError("Expected number or parenthesized expression")

	tree, value = parse_expression()
	if current()["type"] != "END":
		raise ValueError("Unexpected trailing input")
	return tree, value


def evaluate_line(expression: str) -> dict:
	tokens: list[dict] | None = None
	try:
		tokens = tokenize(expression)
		tree, result = evaluate_tokens(tokens)
		return {
			"input": expression,
			"tree": tree,
			"tokens": tokens_to_output(tokens),
			"result": float(result),
		}
	except ValueError as exc:
		message = str(exc)
		if message.startswith("DIV_ZERO::"):
			division_tree = message.split("::", 1)[1]
			return {
				"input": expression,
				"tree": division_tree,
				"tokens": tokens_to_output(tokens) if tokens is not None else "ERROR",
				"result": "ERROR",
			}
		return {
			"input": expression,
			"tree": "ERROR",
			"tokens": "ERROR",
			"result": "ERROR",
		}
	except Exception:
		return {
			"input": expression,
			"tree": "ERROR",
			"tokens": "ERROR",
			"result": "ERROR",
		}


def evaluate_file(input_path: str) -> list[dict]:
	input_file = Path(input_path)
	output_file = input_file.parent / "output.txt"

	lines = input_file.read_text(encoding="utf-8").splitlines()
	if lines:
		lines[0] = lines[0].lstrip("\ufeff")
	results = [evaluate_line(line) for line in lines]

	blocks: list[str] = []
	for item in results:
		if item["result"] == "ERROR":
			result_text = "ERROR"
		else:
			result_text = format_result(item["result"])

		block = "\n".join(
			[
				f"Input: {item['input']}",
				f"Tree: {item['tree']}",
				f"Tokens: {item['tokens']}",
				f"Result: {result_text}",
			]
		)
		blocks.append(block)

	output_file.write_text("\n\n".join(blocks), encoding="utf-8")
	return results


def main() -> None:
	if len(sys.argv) != 2:
		print("Usage: python question2.py <input_file>")
		return

	results = evaluate_file(sys.argv[1])
	print(f"Processed {len(results)} expressions.")


if __name__ == "__main__":
	main()