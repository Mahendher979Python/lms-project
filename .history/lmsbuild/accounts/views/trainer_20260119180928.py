@admin_required
def admin_trainer_list(request):
    trainers = TrainerProfile.objects.select_related("user")
    return render(request, "accounts/admin/trainers/list.html", {
        "trainers": trainers
    })


@admin_required
def admin_trainer_create(request):
    if request.method == "POST":
        user = User.objects.create_user(
            username=request.POST["username"],
            email=request.POST["email"],
            role="trainer",
            password="Temp@123"
        )

        TrainerProfile.objects.create(
            user=user,
            employee_id=request.POST["employee_id"],
            first_name=request.POST["first_name"],
            surname=request.POST["surname"],
            qualification=request.POST["qualification"],
            designation=request.POST["designation"],
            phone=request.POST["phone"],
            address=request.POST["address"],
            joining_date=request.POST["joining_date"]
        )

        return redirect("admin_trainer_list")

    return render(request, "accounts/admin/trainers/create.html")
