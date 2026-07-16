from auth import login
from workflow import validate_workflow, import_workflow
from viewer import view_logs
from logger import log_event
from verifier import verify_dataset_hash
from security_viewer import view_security_events


def display_menu(username, role):
    """
    Display the main menu.
    """

    print("\n")
    print("=" * 55)
    print("      END-TO-END SECURE BIG DATA PIPELINE")
    print("=" * 55)

    print(f"Logged in as : {username}")
    print(f"Role         : {role}")

    print("-" * 55)
    print("1. Validate Dataset")
    print("2. Run Secure Import Pipeline")
    print("3. Verify Dataset Integrity")
    print("4. View Audit Logs")
    print("5. Exit")
    print("-" * 55)


def main():

    # -----------------------------
    # Login
    # -----------------------------

    user = login()

    if user is None:
        print("\nAccess denied.")
        return

    username, role = user

    # -----------------------------
    # Menu Loop
    # -----------------------------

    while True:

        display_menu(username, role)

        choice = input("\nChoose an option: ")

        if choice == "1":

            validate_workflow(
                username,
                role
            )

        elif choice == "2":

            import_workflow(
                username,
                role
            )

        elif choice == "3":

            verify_dataset_hash(
                username,
                role
            )

        elif choice == "4":

            view_logs(
                username,
                role
            )

        elif choice == "5":

            log_event(
                username=username,
                action="User Logout",
                status="SUCCESS"
            )

            print("\nGoodbye!")
            break

        else:

            print("\nInvalid option. Please try again.")


if __name__ == "__main__":
    main()