from uuid import UUID, uuid4

from sqlalchemy import Boolean, ForeignKey, String, UniqueConstraint
from sqlalchemy.orm import Mapped, mapped_column, relationship
from sqlalchemy.dialects.postgresql import UUID as SQLUUID

from enum import StrEnum

from app.db.base import Base


class PullRequestStatus(StrEnum):
    OPEN = "OPEN"
    MERGED = "MERGED"


class Team(Base):
    __tablename__ = "teams"

    id: Mapped[UUID] = mapped_column(SQLUUID, primary_key=True, default=uuid4)

    name: Mapped[str] = mapped_column(String(255), unique=True, nullable=False)

    users: Mapped[list["User"]] = relationship(
        back_populates="team", cascade="all, delete-orphan"
    )


class User(Base):
    __tablename__ = "users"

    id: Mapped[str] = mapped_column(String(100), primary_key=True)

    username: Mapped[str] = mapped_column(String(255), nullable=False)

    is_active: Mapped[bool] = mapped_column(Boolean, nullable=False, default=True)

    team_id: Mapped[UUID] = mapped_column(ForeignKey("teams.id"), nullable=False)

    team: Mapped["Team"] = relationship(back_populates="users")

    authored_pull_requests: Mapped[list["PullRequest"]] = relationship(
        back_populates="author", foreign_keys="PullRequest.author_id"
    )

    reviews: Mapped[list["PullRequestReviewer"]] = relationship(
        back_populates="reviewer"
    )


class PullRequest(Base):
    __tablename__ = "pull_requests"

    id: Mapped[str] = mapped_column(String(100), primary_key=True)

    title: Mapped[str] = mapped_column(String(255), nullable=False)

    status: Mapped[PullRequestStatus] = mapped_column(
        default=PullRequestStatus.OPEN, nullable=False
    )

    author_id: Mapped[str] = mapped_column(ForeignKey("users.id"), nullable=False)

    author: Mapped["User"] = relationship(
        back_populates="authored_pull_requests", foreign_keys=[author_id]
    )

    reviewers: Mapped[list["PullRequestReviewer"]] = relationship(
        back_populates="pull_request",
        cascade="all, delete-orphan",
    )


class PullRequestReviewer(Base):
    __tablename__ = "pull_request_reviewers"

    __table_args__ = (
        UniqueConstraint(
            "pull_request_id", "reviewer_id", name="uq_pull_request_reviewer"
        ),
    )

    id: Mapped[UUID] = mapped_column(SQLUUID, primary_key=True, default=uuid4)

    pull_request_id: Mapped[str] = mapped_column(
        ForeignKey("pull_requests.id"), nullable=False
    )

    reviewer_id: Mapped[str] = mapped_column(ForeignKey("users.id"), nullable=False)

    reviewer: Mapped["User"] = relationship(back_populates="reviews")

    pull_request: Mapped["PullRequest"] = relationship(back_populates="reviewers")
