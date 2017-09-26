import re

def process(tokens, graph, initial_state, actions, result_object):
  state = initial_state

  for token in tokens:
    if state != 'f' and state != None:
      for key, value in graph[state].items():
        if(re.match(key, token)):
            state = value
            if state:
              actions[state](result_object, token)
            break
  return state


def main():
  line = "Dietética de al lado 1234 2222"
  tokens = line.split()
  tokens.append('\0')
  resultado = {}
  ret = process(tokens, GRAPH_ADD_PAYMENT, 's', ACTIONS_ADD_PAYMENT, resultado)
  print(ret)
  print(resultado)


if __name__ == "__main__":
  main()
