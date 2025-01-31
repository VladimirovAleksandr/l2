from django.db import models

from clients.models import Card
from directory.models import Researches
from users.models import DoctorProfile, Speciality
from utils.models import ChoiceArrayField
from directions.models import Napravleniya


class ScheduleResource(models.Model):
    executor = models.ForeignKey(DoctorProfile, db_index=True, null=True, verbose_name='Исполнитель', on_delete=models.SET_NULL)
    service = models.ManyToManyField(Researches, verbose_name='Услуга', db_index=True)  # TODO: может быть несколько
    room = models.ForeignKey(
        'podrazdeleniya.Room', related_name='scheduleresourceroom', verbose_name='Кабинет', db_index=True, blank=True, null=True, default=None, on_delete=models.SET_NULL
    )
    department = models.ForeignKey(
        'podrazdeleniya.Podrazdeleniya', null=True, blank=True, verbose_name='Подразделение', db_index=True, related_name='scheduleresourcedepartment', on_delete=models.CASCADE
    )
    speciality = models.ForeignKey(Speciality, null=True, blank=True, verbose_name='Специальность', db_index=True, on_delete=models.CASCADE)
    hile = models.BooleanField(default=False, blank=True, help_text='Скрытие ресурса', db_index=True)

    def __str__(self):
        return f"{self.pk} — {self.executor} — {self.service} {self.room}, {self.department}, {self.speciality}"

    class Meta:
        verbose_name = 'Ресурс'
        verbose_name_plural = 'Ресурсы'
        ordering = ['-id']


class SlotPlan(models.Model):
    GOSUSLUGI = 'gosuslugi'
    PORTAL = 'portal'
    LOCAL = 'local'

    AVAILABLE_RECORDS = (
        (GOSUSLUGI, 'ЕПГУ'),
        (PORTAL, 'Портал пациента'),
        (LOCAL, 'Текущая система L2'),
    )

    resource = models.ForeignKey(ScheduleResource, db_index=True, verbose_name='Ресурс', on_delete=models.CASCADE)
    datetime = models.DateTimeField(db_index=True, verbose_name='Дата/время слота')
    duration_minutes = models.PositiveSmallIntegerField(verbose_name='Длительность в мин')
    available_systems = ChoiceArrayField(models.CharField(max_length=16, choices=AVAILABLE_RECORDS), verbose_name='Источник записи')
    disabled = models.BooleanField(default=False, blank=True, verbose_name='Не доступно для записи', db_index=True)
    is_cito = models.BooleanField(default=False, blank=True, verbose_name='ЦИТО', db_index=True)

    def __str__(self):
        return f"{self.pk} — {self.datetime} {self.duration_minutes} мин, {self.resource}"

    class Meta:
        verbose_name = 'Слот'
        verbose_name_plural = 'Слоты'
        ordering = ['-id']


class SlotFact(models.Model):
    RESERVED = 0
    CANCELED = 1
    SUCCESS = 2

    STATUS = (
        (CANCELED, "Отмена"),
        (RESERVED, "Зарезервировано"),
        (SUCCESS, "Выполнено"),
    )
    plan = models.ForeignKey(SlotPlan, db_index=True, verbose_name='Слот-план', on_delete=models.CASCADE)
    patient = models.ForeignKey(Card, verbose_name='Карта пациента', db_index=True, null=True, on_delete=models.SET_NULL)
    status = models.PositiveSmallIntegerField(choices=STATUS, blank=True, db_index=True, verbose_name='Статус')
    external_slot_id = models.CharField(max_length=255, default='', blank=True, verbose_name='Внешний ИД')
    service = models.ForeignKey(Researches, verbose_name='Услуга', db_index=True, null=True, blank=True, on_delete=models.CASCADE)
    direction = models.ForeignKey(Napravleniya, verbose_name='Направление', db_index=True, null=True, blank=True, on_delete=models.CASCADE)

    def __str__(self):
        return f"{self.pk} — {self.patient} {self.get_status_display()} {self.plan}"

    class Meta:
        verbose_name = 'Запись на слот'
        verbose_name_plural = 'Записи на слоты'
        ordering = ['-id']
