from django.db import models
from django.utils import timezone

from core.models import User


class Status(models.IntegerChoices):
    TO_DO = 1, "К выполнению"
    IN_PROGRESS = 2, "В процессе"
    DONE = 3, "Выполнено"
    ARCHIVED = 4, "Архив"


class Priority(models.IntegerChoices):
    LOW = 1, "Низкий"
    MEDIUM = 2, "Средний"
    HIGH = 3, "Высокий"
    CRITICAL = 4, "Критический"


class Role(models.IntegerChoices):
    OWNER = 1, "Владелец"
    WRITER = 2, "Редактор"
    READER = 3, "Читатель"


class DatesModelMixin(models.Model):
    class Meta:
        abstract = True  # Помечаем класс как абстрактный – для него не будет таблички в БД

    created = models.DateTimeField(verbose_name="Дата создания", auto_now_add=True)
    updated = models.DateTimeField(verbose_name="Дата последнего обновления", auto_now=True)

    # def save(self, *args, **kwargs):
    #         if not self.id:  # Когда модель только создается – у нее нет id
    #             self.created = timezone.now()
    #         self.updated = timezone.now()  # Каждый раз, когда вызывается save, проставляем свежую дату обновления
    #         return super().save(*args, **kwargs)


class Board(DatesModelMixin):
    class Meta:
        verbose_name = "Доска"
        verbose_name_plural = "Доски"

    title = models.CharField(verbose_name="Название", max_length=255)
    is_deleted = models.BooleanField(verbose_name="Удалена", default=False)


class BoardParticipant(DatesModelMixin):
    class Meta:
        unique_together = ("board", "user")
        verbose_name = "Участник"
        verbose_name_plural = "Участники"


    board = models.ForeignKey(Board, verbose_name="Доска", on_delete=models.PROTECT, related_name="participants")
    user = models.ForeignKey(User, verbose_name="Пользователь", on_delete=models.PROTECT, related_name="participants")
    role = models.PositiveSmallIntegerField(verbose_name="Роль", choices=Role.choices, default=Role.OWNER)


class Category(DatesModelMixin):
    class Meta:
        verbose_name = "Категория"
        verbose_name_plural = "Категории"

    board = models.ForeignKey(Board, verbose_name="Доска", on_delete=models.PROTECT, related_name="categories")
    title = models.CharField(verbose_name="Название", max_length=255)
    user = models.ForeignKey(User, verbose_name="Автор", on_delete=models.PROTECT, related_name="categories")
    is_deleted = models.BooleanField(verbose_name="Удалена", default=False)


class Goal(DatesModelMixin):
    class Meta:
        verbose_name = "Цель"
        verbose_name_plural = "Цели"

    user = models.ForeignKey(User, verbose_name="Автор", on_delete=models.PROTECT, related_name="goals")
    category = models.ForeignKey(Category, verbose_name="Категория", on_delete=models.PROTECT)
    title = models.CharField(verbose_name="Название", max_length=255)
    description = models.TextField(verbose_name="Описание", null=True, blank=True, default=None)
    status = models.PositiveSmallIntegerField(verbose_name="Статус", choices=Status.choices, default=Status.TO_DO)
    priority = models.PositiveSmallIntegerField(verbose_name="Приоритет", choices=Priority.choices,
                                                default=Priority.MEDIUM)
    due_date = models.DateTimeField(verbose_name="Дата дедлайна", null=True, blank=True, default=None)

    # is_deleted = models.BooleanField(verbose_name="Удалена", default=False)

    def __str__(self):
        return self.title


class Comment(DatesModelMixin):
    class Meta:
        verbose_name = "Комментарий"
        verbose_name_plural = "Комментарии"

    user = models.ForeignKey(User, verbose_name="Автор", related_name="goal_comments", on_delete=models.PROTECT)
    goal = models.ForeignKey(Goal, verbose_name="Цель", related_name="goal_comments", on_delete=models.PROTECT)
    text = models.TextField(verbose_name="Текст")
