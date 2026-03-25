import argparse
import builtins
import sys

import blackjackMainTester as tester


class TerminalReplayType:
    """Emit text exactly as the game writes it, but without animation delays."""

    @staticmethod
    def _emit(*words):
        if not words:
            return
        sys.stdout.write("".join(str(word) for word in words))
        sys.stdout.flush()

    def check_for_skip(self):
        return False

    def fast(self, *words):
        self._emit(*words)

    def fast_clean(self, *words):
        self._emit(*words)

    def slow(self, *words):
        self._emit(*words)

    def slow_clean(self, *words):
        self._emit(*words)

    def suspense(self, *words):
        self._emit(*words)

    def suspense_clean(self, *words):
        self._emit(*words)

    def type(self, *words):
        self._emit(*words)

    def type_clean(self, *words):
        self._emit(*words)

    def typeover(self, prompt, text, newline=False):
        sys.stdout.write(str(prompt))
        sys.stdout.flush()
        sys.stdout.write("\r" + (" " * len(str(prompt))) + "\r")
        sys.stdout.flush()
        self._emit(str(text))
        if newline:
            sys.stdout.write("\n")
            sys.stdout.flush()

    def cleanup(self):
        return None


class EchoSeededController(tester.SeededAsk):
    """Deterministic input source that echoes responses like a real terminal session."""

    def _echo(self, prompt, value):
        sys.stdout.write(str(prompt) + str(value))
        sys.stdout.write("\n")
        sys.stdout.flush()

    def _pick_text(self, prompt):
        prompt_text = str(prompt or "")
        prompt_lower = prompt_text.lower()
        if "color" in prompt_lower:
            options = ["blue", "red", "green", "black", "silver"]
        elif "animal" in prompt_lower:
            options = ["fox", "crow", "dog", "rabbit", "cat"]
        elif "name" in prompt_lower:
            options = ["Alex", "Sam", "Jordan", "Taylor", "Morgan"]
        elif "casino" in prompt_lower:
            options = ["Lucky Strike", "Golden Mirage", "Last Chance", "Neon Pit"]
        else:
            options = ["test", "ok", "yes", "no", "pass"]
        value = options[self._idx(f"raw_text:{prompt_text}:{'|'.join(options)}", len(options))]
        self._record("raw_input", prompt_text, value)
        return value

    def _pick_cash(self, prompt):
        prompt_text = str(prompt or "")
        prompt_lower = prompt_text.lower()
        if "bet" in prompt_lower:
            options = [50, 100, 250, 500]
        elif "offer" in prompt_lower:
            options = [25, 50, 100, 200]
        else:
            options = [0, 1, 5, 10, 25, 50, 100]
        value = options[self._idx(f"raw_cash:{prompt_text}:{'|'.join(str(o) for o in options)}", len(options))]
        self._record("raw_input", prompt_text, value)
        return str(value)

    def raw_input(self, prompt=""):
        prompt_text = str(prompt or "")
        prompt_lower = prompt_text.lower()
        if "$" in prompt_text or any(token in prompt_lower for token in ["bet", "amount", "offer", "cash"]):
            value = self._pick_cash(prompt_text)
        elif prompt_text == "":
            value = ""
            self._record("raw_input", prompt_text, value)
        else:
            value = self._pick_text(prompt_text)
        self._echo(prompt_text, value)
        return value


class ReplayAsk:
    """Faithful Ask replacement that preserves prompt spacing while auto-answering."""

    def __init__(self, controller, replay_type):
        self._controller = controller
        self._type = replay_type

    def single_word(self, prompt=""):
        value = self._controller.single_word(prompt)
        self._controller._echo(prompt, value)
        if value:
            return str(value).split()[0]
        return ""

    def choose_a_number(self, a, b, guess=False):
        if guess:
            self._type.fast_clean("What's your guess? ")
        else:
            self._type.fast_clean("Choose a number between " + str(a) + " and " + str(b) + ": ")
        value = self._controller.choose_a_number(a, b, guess=guess)
        self._controller._echo("", value)
        return int(value)

    def choose_an_option(self, options, reiterate="What? ", first_letter=True):
        value = self._controller.choose_an_option(options, reiterate=reiterate, first_letter=first_letter)
        self._controller._echo("", value)
        return value

    def option(self, prompt, options):
        labels = [str(option).strip() for option in options]
        option_text = "/".join(labels)
        prompt_text = str(prompt).strip()
        if prompt_text:
            if prompt_text.endswith(":"):
                rendered_prompt = prompt_text + " [" + option_text + "] "
            else:
                rendered_prompt = prompt_text + " [" + option_text + "]: "
        else:
            rendered_prompt = "Choose [" + option_text + "]: "
        value = self._controller.option(prompt, labels)
        self._controller._echo(rendered_prompt, value)
        return value

    def yes_or_no(self, reiterate="What? "):
        value = self._controller.yes_or_no(reiterate=reiterate)
        self._controller._echo("", value)
        print()
        return value

    def give_cash(self, total, reiterate="How much? "):
        value = self._controller.give_cash(total, reiterate=reiterate)
        self._controller._echo("", value)
        print("")
        return value

    def press_continue(self, message="Press any key to continue: "):
        self._type.type(message)
        return None

    def continue_cleanup(self):
        return True


def _patch_module_attr(attr_name, replacement):
    patched = []
    for module_name, module in list(sys.modules.items()):
        if module is None:
            continue
        if not (
            module_name == "story"
            or module_name.startswith("story.")
            or module_name == "blackjack"
            or module_name.startswith("blackjack.")
        ):
            continue
        if hasattr(module, attr_name):
            old_value = getattr(module, attr_name)
            setattr(module, attr_name, replacement)
            patched.append((module, old_value))
    return patched


def _restore_module_attr(patched, attr_name):
    for module, old_value in patched:
        setattr(module, attr_name, old_value)


def _resolve_testers(event_names):
    name_to_callable = {fn.__name__: fn for fn in tester.ALL_EVENT_TESTERS}
    if not event_names:
        return list(tester.ALL_EVENT_TESTERS)

    selected = []
    for name in event_names:
        fn = name_to_callable.get(name)
        if fn is None:
            print(tester.bright(tester.red("UNKNOWN TESTER: " + str(name))))
            continue
        selected.append(fn)
    return selected


def run_batch(event_names=None, seed_start=1, seed_count=1, show_trace=False, stop_on_error=False):
    selected = _resolve_testers(event_names)
    if not selected:
        return 1

    original_input = builtins.input
    replay_type = TerminalReplayType()

    for seed in range(int(seed_start), int(seed_start) + int(seed_count)):
        print(tester.bright(tester.red("SEED RUN " + str(seed))))
        controller = EchoSeededController(seed)
        replay_ask = ReplayAsk(controller, replay_type)
        patched_ask = _patch_module_attr("ask", replay_ask)
        patched_type = _patch_module_attr("type", replay_type)
        tester.ACTIVE_TEST_SEED = int(seed)
        tester.ACTIVE_TEST_SEED_COUNTER = 0
        builtins.input = controller.raw_input
        try:
            for fn in selected:
                before = len(tester.REROUTE_LOG)
                print(tester.bright(tester.red("TESTER " + fn.__name__ + " (seed " + str(seed) + ")")))
                try:
                    fn()
                except Exception as exc:
                    print(tester.bright(tester.red("TESTER FAILED: " + fn.__name__ + " -> " + repr(exc))))
                    if stop_on_error:
                        raise
                after = len(tester.REROUTE_LOG)
                if after > before:
                    print(tester.bright(tester.red("REROUTE SUMMARY for " + fn.__name__ + ": " + str(after - before) + " blocked redirect(s)")))
        finally:
            builtins.input = original_input
            tester.ACTIVE_TEST_SEED = None
            tester.ACTIVE_TEST_SEED_COUNTER = 0
            _restore_module_attr(patched_ask, "ask")
            _restore_module_attr(patched_type, "type")

        if show_trace and controller.trace:
            print(tester.bright(tester.red("SEED " + str(seed) + " DECISION TRACE")))
            for index, (kind, prompt, choice) in enumerate(controller.trace, start=1):
                print(tester.red(f"  [{index}] {kind} | {prompt} -> {choice}"))

    return 0


def main():
    parser = argparse.ArgumentParser(description="Batch-run blackjack event testers with echoed terminal input.")
    parser.add_argument("events", nargs="*", help="Optional tester function names to run. Default: run all testers.")
    parser.add_argument("--seed-start", type=int, default=1, help="First seed to run.")
    parser.add_argument("--seed-count", type=int, default=1, help="Number of sequential seeds to run.")
    parser.add_argument("--trace", action="store_true", help="Print the deterministic decision trace after each seed.")
    parser.add_argument("--stop-on-error", action="store_true", help="Stop immediately when a tester fails.")
    args = parser.parse_args()
    raise SystemExit(
        run_batch(
            event_names=args.events,
            seed_start=args.seed_start,
            seed_count=args.seed_count,
            show_trace=args.trace,
            stop_on_error=args.stop_on_error,
        )
    )


if __name__ == "__main__":
    main()